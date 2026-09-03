<?php
/* Checking a Google ID token, with nothing installed.
 *
 * The browser gets a signed JWT from Google and posts it here. We verify the
 * signature against Google's published RSA keys and then read the claims. That
 * means there is no client secret in this app at all, and nothing to leak.
 *
 * Never trust a claim before the signature checks out. The payload is
 * attacker supplied until openssl says otherwise, so the order below matters.
 */
declare(strict_types=1);

const GOOGLE_CERTS = 'https://www.googleapis.com/oauth2/v3/certs';
const GOOGLE_ISS   = ['accounts.google.com', 'https://accounts.google.com'];
const CLOCK_SKEW   = 120;

function b64url(string $s): string {
    $out = base64_decode(strtr($s, '-_', '+/'), true);
    return $out === false ? '' : $out;
}

/* DER helpers. Just enough ASN.1 to turn a JWK into a PEM public key. */
function der_len(int $n): string {
    if ($n < 0x80) return chr($n);
    $b = ltrim(pack('N', $n), "\x00");
    return chr(0x80 | strlen($b)) . $b;
}
function der_int(string $raw): string {
    $raw = ltrim($raw, "\x00");
    if ($raw === '') $raw = "\x00";
    /* A leading high bit would read as negative, so pad it. */
    if (ord($raw[0]) & 0x80) $raw = "\x00" . $raw;
    return "\x02" . der_len(strlen($raw)) . $raw;
}
function der_seq(string $body): string {
    return "\x30" . der_len(strlen($body)) . $body;
}

function jwk_to_pem(array $jwk): ?string {
    if (($jwk['kty'] ?? '') !== 'RSA') return null;
    $n = b64url($jwk['n'] ?? '');
    $e = b64url($jwk['e'] ?? '');
    if ($n === '' || $e === '') return null;
    $rsa = der_seq(der_int($n) . der_int($e));
    /* SubjectPublicKeyInfo: the rsaEncryption OID, a NULL, then the key in a
       BIT STRING with a zero unused-bits byte in front of it. */
    $oid = "\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x01\x01" . "\x05\x00";
    $bit = "\x03" . der_len(strlen($rsa) + 1) . "\x00" . $rsa;
    $der = der_seq(der_seq($oid) . $bit);
    return "-----BEGIN PUBLIC KEY-----\n"
         . chunk_split(base64_encode($der), 64, "\n")
         . "-----END PUBLIC KEY-----\n";
}

function cache_path(string $name): string {
    $c = cfg();
    $dir = $c['cache_dir'] ?: (dirname(__DIR__, 2) . '/lockedin-cache');
    if (!is_dir($dir)) @mkdir($dir, 0770, true);
    if (!is_writable($dir)) $dir = sys_get_temp_dir();
    return rtrim($dir, '/') . '/' . $name;
}

function http_get(string $url): ?string {
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 8,
            CURLOPT_CONNECTTIMEOUT => 4,
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_SSL_VERIFYHOST => 2,
            CURLOPT_FOLLOWLOCATION => false,
        ]);
        $out = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
        return ($out !== false && $code === 200) ? (string) $out : null;
    }
    $out = @file_get_contents($url, false, stream_context_create([
        'http' => ['timeout' => 8, 'ignore_errors' => true],
        'ssl'  => ['verify_peer' => true, 'verify_peer_name' => true],
    ]));
    return $out === false ? null : $out;
}

/* Google rotates these keys. Cached for a day, refetched on demand when a
   token arrives signed by a kid we have not seen. */
function google_keys(bool $force = false): array {
    $path = cache_path('google-certs.json');
    if (!$force && is_file($path) && (time() - (int) filemtime($path)) < 86400) {
        $hit = json_decode((string) file_get_contents($path), true);
        if (is_array($hit) && !empty($hit['keys'])) return $hit['keys'];
    }
    $raw = http_get(GOOGLE_CERTS);
    if ($raw === null) {
        /* Network trouble should not log everyone out, so a stale cache still
           counts if we have one. */
        if (is_file($path)) {
            $hit = json_decode((string) file_get_contents($path), true);
            if (is_array($hit) && !empty($hit['keys'])) return $hit['keys'];
        }
        return [];
    }
    $set = json_decode($raw, true);
    if (!is_array($set) || empty($set['keys'])) return [];
    @file_put_contents($path, $raw, LOCK_EX);
    return $set['keys'];
}

function find_key(string $kid, bool $force = false): ?array {
    foreach (google_keys($force) as $k) {
        if (($k['kid'] ?? '') === $kid) return $k;
    }
    return $force ? null : find_key($kid, true);
}

/* Returns the claims, or null if anything at all is wrong. Callers get no
   detail about which check failed, because that detail is only useful to
   somebody probing it. */
function verify_google_token(string $jwt, string $clientId): ?array {
    if ($clientId === '') return null;
    $parts = explode('.', $jwt);
    if (count($parts) !== 3) return null;
    [$h64, $p64, $s64] = $parts;

    $head = json_decode(b64url($h64), true);
    if (!is_array($head) || ($head['alg'] ?? '') !== 'RS256') return null;
    $kid = $head['kid'] ?? '';
    if (!is_string($kid) || $kid === '') return null;

    $jwk = find_key($kid);
    if ($jwk === null) return null;
    $pem = jwk_to_pem($jwk);
    if ($pem === null) return null;

    $sig = b64url($s64);
    if ($sig === '') return null;
    $okSig = openssl_verify($h64 . '.' . $p64, $sig, $pem, OPENSSL_ALGO_SHA256);
    if ($okSig !== 1) return null;

    $c = json_decode(b64url($p64), true);
    if (!is_array($c)) return null;

    if (!in_array((string) ($c['iss'] ?? ''), GOOGLE_ISS, true)) return null;
    if (!hash_equals($clientId, (string) ($c['aud'] ?? ''))) return null;
    $nowT = time();
    if ((int) ($c['exp'] ?? 0) < $nowT - CLOCK_SKEW) return null;
    if ((int) ($c['iat'] ?? 0) > $nowT + CLOCK_SKEW) return null;
    if (($c['sub'] ?? '') === '') return null;

    /* An unverified address is somebody else's until Google says otherwise,
       and letting one in would hand over any account that shares it. */
    $verified = $c['email_verified'] ?? false;
    if ($verified !== true && $verified !== 'true') return null;
    if (!filter_var((string) ($c['email'] ?? ''), FILTER_VALIDATE_EMAIL)) return null;

    return $c;
}
