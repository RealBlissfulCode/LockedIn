<?php
/* Test harness: stand in for Google. Makes a keypair, publishes it where the
   app caches Google's JWKS, and mints signed ID tokens on demand. */
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

$opt = json_decode($argv[1] ?? '{}', true) ?: [];
$now = time();
$claims = array_merge([
    'iss' => 'https://accounts.google.com',
    'aud' => 'test-client-id.apps.googleusercontent.com',
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
