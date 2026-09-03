<?php
/* Sessions. A random token goes in an httponly cookie, and only its sha256
   lands in the database, so a leaked table dump cannot be replayed. */
declare(strict_types=1);

const SESS_COOKIE = 'li_session';
const SESS_DAYS   = 60;

function token_hash(string $t): string {
    return hash('sha256', $t);
}

function start_session(int $accountId): string {
    $tok = bin2hex(random_bytes(32));
    q('INSERT INTO sessions (token_hash, account_id, created_at, expires_at, seen_at, ua)
       VALUES (?, ?, ?, ?, ?, ?)',
       [token_hash($tok), $accountId, now(), in_days(SESS_DAYS), now(),
        substr((string) ($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 255)]);
    set_session_cookie($tok, time() + SESS_DAYS * 86400);
    return $tok;
}

function set_session_cookie(string $value, int $expires): void {
    if (headers_sent()) return;
    setcookie(SESS_COOKIE, $value, [
        'expires'  => $expires,
        'path'     => '/',
        'secure'   => (bool) (cfg()['secure_cookies'] ?? true),
        'httponly' => true,
        /* Lax keeps the cookie off cross site POSTs while still surviving a
           normal link back into the app. */
        'samesite' => 'Lax',
    ]);
}

function end_session(): void {
    $tok = $_COOKIE[SESS_COOKIE] ?? '';
    if (is_string($tok) && $tok !== '') {
        q('DELETE FROM sessions WHERE token_hash = ?', [token_hash($tok)]);
    }
    set_session_cookie('', time() - 3600);
}

/* The signed in account, or null. Touches seen_at at most once an hour so a
   busy tab is not writing on every request. */
function current_account(): ?array {
    static $cached = false, $acct = null;
    if ($cached) return $acct;
    $cached = true;

    $tok = $_COOKIE[SESS_COOKIE] ?? '';
    if (!is_string($tok) || strlen($tok) !== 64) return null;

    $row = one('SELECT s.token_hash, s.seen_at, a.*
                  FROM sessions s
                  JOIN accounts a ON a.id = s.account_id
                 WHERE s.token_hash = ? AND s.expires_at > ?',
               [token_hash($tok), now()]);
    if ($row === null) return null;

    if (strtotime((string) $row['seen_at']) < time() - 3600) {
        q('UPDATE sessions SET seen_at = ? WHERE token_hash = ?', [now(), $row['token_hash']]);
        q('UPDATE accounts SET last_seen_at = ? WHERE id = ?', [now(), $row['id']]);
    }
    unset($row['token_hash'], $row['seen_at']);
    $acct = $row;
    return $acct;
}

function need_account(): array {
    $a = current_account();
    if ($a === null) fail(401, 'signed_out');
    return $a;
}

/* Housekeeping, run on the way through sign in. Cheap and keeps the table from
   growing forever on a host with no cron. */
function sweep_expired(): void {
    if (random_int(1, 50) !== 1) return;
    q('DELETE FROM sessions WHERE expires_at < ?', [now()]);
    q('DELETE FROM invites WHERE used_by IS NULL AND expires_at < ?', [in_days(-30)]);
}
