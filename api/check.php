<?php
/* Setup check. Open /api/check.php in a browser after deploying.
 *
 * It exists because "Sign in failed" tells you nothing and the thing that has
 * actually gone wrong is almost always one of six boring problems. This names
 * which one. It prints no passwords, no database name, no host, and it masks
 * the client id, so the worst it can tell a stranger is which boxes are ticked.
 *
 * Once the first account exists it stops answering unless you are signed in,
 * so it does not sit open forever on a live site.
 */
declare(strict_types=1);
require __DIR__ . '/lib/http.php';

$rows = [];
function check(string $name, bool $pass, string $detail = '', string $fix = ''): void {
    global $rows;
    $rows[] = ['name' => $name, 'pass' => $pass, 'detail' => $detail, 'fix' => $fix];
}

/* ---- PHP itself ---- */
check('PHP 8.0 or newer', PHP_VERSION_ID >= 80000, 'Running ' . PHP_VERSION,
      'Set the PHP version to 8.1 or later in hPanel, Advanced, PHP Configuration.');
foreach (['pdo_mysql' => 'talking to MySQL',
          'openssl'   => 'checking the signature on a Google token',
          'curl'      => 'fetching Google signing keys',
          'mbstring'  => 'handling names with accents in them'] as $ext => $why) {
    check('Extension ' . $ext, extension_loaded($ext), 'Needed for ' . $why,
          'Enable ' . $ext . ' in hPanel, Advanced, PHP Configuration, PHP extensions.');
}

/* ---- config ---- */
$cfgPath = __DIR__ . '/config.php';
$haveCfg = is_file($cfgPath);
check('api/config.php exists', $haveCfg, $haveCfg ? '' : 'Not found',
      'Copy api/config.sample.php to api/config.php on the server and fill it in.');

$c = $haveCfg ? (require $cfgPath) : null;
$cfgOk = is_array($c);
check('config.php returns settings', $cfgOk, '',
      'The file has to end with a return [ ... ]; and nothing may print before it.');

$clientId = $cfgOk ? (string) ($c['google_client_id'] ?? '') : '';
check('Google client id set', $clientId !== '',
      $clientId === '' ? 'Empty' : 'Ends ' . substr($clientId, -14),
      'Paste the OAuth client id from Google Cloud Console into config.php.');

/* ---- database ---- */
$pdo = null;
$dbErr = '';
$dbFix = '';
if ($cfgOk) {
    try {
        $pdo = new PDO(
            sprintf('mysql:host=%s;dbname=%s;charset=utf8mb4', $c['db_host'] ?? '', $c['db_name'] ?? ''),
            (string) ($c['db_user'] ?? ''), (string) ($c['db_pass'] ?? ''),
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_TIMEOUT => 5]
        );
    } catch (Throwable $e) {
        /* MySQL puts the username and the host in the message, so the message
           itself never goes on screen. It is only read here to work out which
           of the four things is wrong, because "check your settings" is not
           advice when there are four of them. */
        $msg = $e->getMessage();
        $code = (string) ($e->getCode() ?: '');
        if (str_contains($msg, '1045') || $code === '1045' || $code === '28000') {
            $dbErr = 'Access denied. The username or the password is wrong.';
            $dbFix = 'In hPanel go to Databases, Management. The list there shows the real '
                   . 'database name and the real username, and both start with your account '
                   . 'prefix, so they look like u123456789_lockedin rather than lockedin. '
                   . 'Copy them exactly. If you cannot remember the password, use Change '
                   . 'password on that user and paste the new one into config.php.';
        } elseif (str_contains($msg, '1049') || str_contains($msg, 'Unknown database')) {
            $dbErr = 'Connected to MySQL, but there is no database with that name.';
            $dbFix = 'db_name has to be the full name from hPanel, Databases, Management, '
                   . 'including the account prefix.';
        } elseif (str_contains($msg, '1044')) {
            $dbErr = 'That user exists but has no rights on that database.';
            $dbFix = 'In hPanel, Databases, Management, check the user is attached to this '
                   . 'database with all privileges.';
        } elseif (str_contains($msg, '2002') || str_contains($msg, '2005')
               || str_contains($msg, 'No such file') || str_contains($msg, 'Unknown MySQL server')) {
            $dbErr = 'Cannot reach a MySQL server at that host.';
            $dbFix = 'On Hostinger db_host is localhost, even though hPanel shows a longer '
                   . 'hostname next to the database.';
        } else {
            $dbErr = 'SQLSTATE ' . ($code ?: '?');
            $dbFix = 'Check db_host, db_name, db_user and db_pass in config.php against '
                   . 'hPanel, Databases, Management.';
        }
    }
}
check('Database connects', $pdo !== null, $dbErr, $dbFix);

/* Only worth saying when the connection actually failed, and it is the single
   most common reason it does. Neither value is printed, only its shape. */
if ($cfgOk && $pdo === null) {
    $u = (string) ($c['db_user'] ?? '');
    $n = (string) ($c['db_name'] ?? '');
    $looksPrefixed = (bool) preg_match('/^u\d+_/', $u) && (bool) preg_match('/^u\d+_/', $n);
    check('Username and database look prefixed', $looksPrefixed,
          $looksPrefixed
            ? 'Both start with an account prefix'
            : 'One of them has no u..._ prefix on it',
          'Shared hosting almost always prefixes both, so the real values look like '
          . 'u123456789_lockedin. Using the short name you typed when creating them is '
          . 'the usual cause of access denied.');
}

$want = ['accounts', 'households', 'members', 'invites', 'docs', 'sessions'];
$have = [];
$anyAccount = false;
if ($pdo !== null) {
    foreach ($pdo->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN) as $t) $have[] = $t;
    $missing = array_values(array_diff($want, $have));
    check('Tables created', !$missing,
          $missing ? 'Missing: ' . implode(', ', $missing) : count($want) . ' tables present',
          'Run php api/migrate.php over SSH. No SSH: put a random string in '
          . 'api/.migrate-key, open /api/migrate.php?key=thatstring, then delete the file.');
    if (!$missing) {
        try {
            $anyAccount = (int) $pdo->query('SELECT COUNT(*) FROM accounts')->fetchColumn() > 0;
        } catch (Throwable $e) { /* counted as fresh */ }
    }
} else {
    check('Tables created', false, 'Cannot look without a database connection', '');
}

/* Once somebody has signed up this page is no longer a setup aid. */
if ($anyAccount) {
    require __DIR__ . '/lib/db.php';
    require __DIR__ . '/lib/google.php';
    require __DIR__ . '/lib/auth.php';
    if (current_account() === null) {
        http_response_code(403);
        header('Content-Type: text/plain; charset=utf-8');
        echo "This check is only open until the first account is created. Sign in first.\n";
        exit;
    }
}

/* ---- can this server reach Google ---- */
$certs = null;
if (function_exists('curl_init')) {
    $ch = curl_init('https://www.googleapis.com/oauth2/v3/certs');
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8,
                            CURLOPT_SSL_VERIFYPEER => true]);
    $body = curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $cerr = curl_error($ch);
    curl_close($ch);
    $certs = ($body !== false && $code === 200 && str_contains((string) $body, '"kid"'));
    check('Can reach Google signing keys', (bool) $certs,
          $certs ? 'Fetched and readable' : ('HTTP ' . $code . ' ' . $cerr),
          'Outbound HTTPS is blocked. Hostinger allows it by default; if it is off, '
          . 'sign in cannot work because the token signature cannot be checked.');
}

/* ---- somewhere to cache them ---- */
$dir = ($cfgOk ? ($c['cache_dir'] ?? null) : null) ?: (dirname(__DIR__, 2) . '/lockedin-cache');
if (!is_dir($dir)) @mkdir($dir, 0770, true);
$writable = is_dir($dir) && is_writable($dir);
check('Somewhere to cache keys', $writable || is_writable(sys_get_temp_dir()),
      $writable ? 'Using the configured directory' : 'Falling back to the temp directory', '');

/* ---- served over https ---- */
$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
      || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
check('Served over https', $https, $https ? '' : 'This request came in over plain http',
      'Google sign in only works on https. Turn on the free SSL certificate in hPanel.');
if ($cfgOk && !$https && ($c['secure_cookies'] ?? true)) {
    check('Cookie setting matches', false, 'secure_cookies is true but this is not https',
          'Either turn on https, which is the right answer, or set secure_cookies to false.');
}

/* ---- config.php must not be readable over the web ---- */
$self = ($https ? 'https://' : 'http://') . ($_SERVER['HTTP_HOST'] ?? '')
      . rtrim(dirname((string) ($_SERVER['REQUEST_URI'] ?? '')), '/');
$leak = null;
/* Skipped under php -S, which serves one request at a time and would sit here
   waiting for itself until the timeout. Apache and LiteSpeed, which is what
   this actually runs on, handle it fine. */
$selfCheckable = php_sapi_name() !== 'cli-server';
if ($selfCheckable && function_exists('curl_init') && ($_SERVER['HTTP_HOST'] ?? '') !== '') {
    $ch = curl_init($self . '/config.php');
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 6,
                            CURLOPT_SSL_VERIFYPEER => false]);
    $b = curl_exec($ch);
    $st = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    /* A 200 that returns nothing is PHP running it, which is fine. A 200 with
       the source in it is not. */
    $leak = ($st === 200 && is_string($b) && str_contains($b, 'db_pass'));
    check('config.php is not readable', !$leak,
          $leak ? 'It came back with the password in it' : 'Not served as text',
          'api/.htaccess should stop this. If your host ignores it, move config.php '
          . 'above the web root and point the require at it.');
}

$failed = array_values(array_filter($rows, fn($r) => !$r['pass']));

if (($_GET['json'] ?? '') === '1') {
    send($failed ? 500 : 200, ['ok' => !$failed, 'checks' => $rows]);
}

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
?><!doctype html><meta charset="utf-8"><title>LockedIn setup check</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;padding:40px 20px;background:#0A0A0C;color:#EDEAF2;
font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}
main{max-width:760px;margin:0 auto}
h1{font-size:26px;letter-spacing:-.02em;margin:0 0 6px}
.sub{color:#8B8796;margin:0 0 28px}
.row{display:flex;gap:14px;padding:14px 0;border-top:1px solid #26262F;align-items:flex-start}
.mark{flex:none;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;
font-size:12px;font-weight:700;margin-top:2px}
.yes{background:rgba(74,222,128,.15);color:#4ADE80}
.no{background:rgba(248,113,113,.15);color:#F87171}
.name{font-weight:600}
.detail{color:#8B8796;font-size:13.5px;margin-top:2px}
.fix{color:#C084FC;font-size:13.5px;margin-top:6px}
.banner{padding:16px 18px;border-radius:10px;margin-bottom:26px;
border:1px solid #26262F;border-left:2px solid #A855F7;background:#131318}
.banner.bad{border-left-color:#F87171}
.banner.good{border-left-color:#4ADE80}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;color:#C084FC}
</style>
<main>
<h1>Setup check</h1>
<p class="sub">Everything the server needs before anybody can sign in.</p>
<?php if ($failed): ?>
  <div class="banner bad"><b><?= count($failed) ?> thing<?= count($failed) === 1 ? '' : 's' ?>
  to fix.</b> Sign in will keep failing until <?= count($failed) === 1 ? 'it is' : 'they are' ?>
  sorted. Each one below says what to do.</div>
<?php else: ?>
  <div class="banner good"><b>All clear.</b> If sign in still fails, the problem is on the
  Google side: add <code><?= htmlspecialchars(($https ? 'https://' : 'http://') . ($_SERVER['HTTP_HOST'] ?? '')) ?></code>
  to Authorized JavaScript origins on your OAuth client, and make sure the consent
  screen is published.</div>
<?php endif; ?>
<?php foreach ($rows as $r): ?>
  <div class="row">
    <span class="mark <?= $r['pass'] ? 'yes' : 'no' ?>"><?= $r['pass'] ? '&check;' : '!' ?></span>
    <div>
      <div class="name"><?= htmlspecialchars($r['name']) ?></div>
      <?php if ($r['detail']): ?><div class="detail"><?= htmlspecialchars($r['detail']) ?></div><?php endif; ?>
      <?php if (!$r['pass'] && $r['fix']): ?><div class="fix"><?= htmlspecialchars($r['fix']) ?></div><?php endif; ?>
    </div>
  </div>
<?php endforeach; ?>
</main>
