<?php
/* Request and response plumbing. Every endpoint speaks JSON and nothing else,
   and no endpoint sends a CORS header. Same origin only, on purpose. */
declare(strict_types=1);

function send(int $code, array $body): never {
    /* Bin anything that leaked out before us, so the reply is JSON and only
       JSON even if something upstream printed a warning. */
    while (ob_get_level() > 0) ob_end_clean();
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    header('X-Robots-Tag: noindex, nofollow');
    echo json_encode($body, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function fail(int $code, string $why, array $extra = []): never {
    send($code, ['ok' => false, 'error' => $why] + $extra);
}

function ok(array $body = []): never {
    send(200, ['ok' => true] + $body);
}

/* Decoded JSON body, or an empty array. Anything that is not an object is a
   client bug, so it gets rejected rather than coerced. */
function body(): array {
    $raw = file_get_contents('php://input');
    if ($raw === false || $raw === '') return [];
    $in = json_decode($raw, true);
    if (!is_array($in)) fail(400, 'bad_json');
    return $in;
}

function str_field(array $in, string $key, int $max, string $default = ''): string {
    $v = $in[$key] ?? $default;
    if (!is_string($v)) fail(400, 'bad_field', ['field' => $key]);
    $v = trim($v);
    if (mb_strlen($v) > $max) $v = mb_substr($v, 0, $max);
    return $v;
}

function method(): string {
    return $_SERVER['REQUEST_METHOD'] ?? 'GET';
}

function need_post(): void {
    if (method() !== 'POST') fail(405, 'post_only');
}

/* Anything that changes state carries a header the browser will only send from
   our own script. A cross site form post cannot set it, so this is the whole
   CSRF defence and it is enough given SameSite=Lax on the cookie. */
function need_xhr(): void {
    if (($_SERVER['HTTP_X_LOCKEDIN'] ?? '') !== '1') fail(403, 'bad_origin');
}
