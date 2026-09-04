<?php
/* Stands in for Google in the tests. Makes a keypair, publishes it where the
   app caches Google's signing keys, and mints signed ID tokens on demand, so
   the real verification code runs against them rather than being stubbed. */
function b64u(string $s): string { return rtrim(strtr(base64_encode($s), '+/', '-_'), '='); }

$keyFile = '/tmp/li-cache/testkey.pem';
if (!is_file($keyFile)) {
    $res = openssl_pkey_new(['private_key_bits' => 2048, 'private_key_type' => OPENSSL_KEYTYPE_RSA]);
    openssl_pkey_export($res, $priv);
    file_put_contents($keyFile, $priv);
}
$priv = file_get_contents($keyFile);
$det  = openssl_pkey_get_details(openssl_pkey_get_private($priv));
$kid  = 'testkid1';
file_put_contents('/tmp/li-cache/google-certs.json', json_encode(['keys' => [[
    'kty' => 'RSA', 'alg' => 'RS256', 'use' => 'sig', 'kid' => $kid,
    'n' => b64u($det['rsa']['n']), 'e' => b64u($det['rsa']['e']),
]]]));

/* Take the audience from the app's own config, so changing the client id in
   one place never quietly breaks every test. */
$cfg = @include dirname(__DIR__) . '/api/config.php';
$aud = is_array($cfg) ? ($cfg['google_client_id'] ?? '') : '';
if ($aud === '') $aud = 'test-client-id.apps.googleusercontent.com';

$opt = json_decode($argv[1] ?? '{}', true) ?: [];
$now = time();
$claims = array_merge([
    'iss' => 'https://accounts.google.com',
    'aud' => $aud,
    'sub' => '110000000000000000001',
    'email' => 'jaronnorris7@gmail.com',
    'email_verified' => true,
    'name' => 'Jaron Norris',
    'picture' => 'https://example.invalid/a.jpg',
    'iat' => $now, 'exp' => $now + 3600,
], $opt);
$head = ['alg' => 'RS256', 'kid' => $opt['__kid'] ?? $kid, 'typ' => 'JWT'];
unset($claims['__kid']);
$signing = b64u(json_encode($head)) . '.' . b64u(json_encode($claims));
openssl_sign($signing, $sig, $priv, OPENSSL_ALGO_SHA256);
if (!empty($opt['__breaksig'])) { unset($claims['__breaksig']); $sig = strrev($sig); }
echo $signing . '.' . b64u($sig);
