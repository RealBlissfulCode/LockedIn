<?php
/* The state documents.
 *
 * GET  ?scope=shared            read one
 * GET  ?do=all                  read the shared one and my private one together
 * POST ?scope=shared            write one, with the version you last read
 *
 * A scope you are not allowed to name is a 403, not an empty result, so a
 * client bug looks like a bug instead of like missing data. */
require __DIR__ . '/boot.php';

$a  = need_account();
$me = (int) $a['id'];
$h  = my_household($me);
if ($h === null) fail(404, 'no_household');
$houseId = (int) $h['id'];

$do = $_GET['do'] ?? '';

if ($do === 'all' && method() === 'GET') {
    ok(['shared'  => read_doc($houseId, 'shared'),
        'private' => read_doc($houseId, 'private:' . $me)]);
}

/* Version numbers and nothing else. The app asks for this every few seconds so
   the other person's edits turn up while you are looking at the page, and it
   has to stay cheap enough to ask that often: two integers, no document. */
if ($do === 'ver' && method() === 'GET') {
    $rows = all('SELECT scope, version FROM docs WHERE household_id = ? AND scope IN (?, ?)',
                [$houseId, 'shared', 'private:' . $me]);
    $out = ['shared' => 0, 'private' => 0];
    foreach ($rows as $r) {
        $out[$r['scope'] === 'shared' ? 'shared' : 'private'] = (int) $r['version'];
    }
    ok($out);
}

$scope = (string) ($_GET['scope'] ?? 'shared');
if (!scope_allowed($scope, $me)) fail(403, 'bad_scope');

/* Reading a previous version back. This exists because a client once sent an
   empty document over a real one, and without history that was the end of it. */
if ($do === 'history' && method() === 'GET') {
    ok(['versions' => all('SELECT version, weight, saved_at FROM doc_history
                            WHERE household_id = ? AND scope = ?
                         ORDER BY version DESC LIMIT 40', [$houseId, $scope])]);
}
if ($do === 'restore') {
    need_post(); need_xhr();
    $v = (int) (body()['version'] ?? 0);
    $row = one('SELECT body FROM doc_history WHERE household_id = ? AND scope = ? AND version = ?',
               [$houseId, $scope, $v]);
    if ($row === null) fail(404, 'no_such_version');
    $b = json_decode((string) $row['body'], true);
    if (!is_array($b)) fail(422, 'unreadable');
    $b['__confirmWipe'] = true;
    $cur = read_doc($houseId, $scope);
    $res = write_doc($houseId, $scope, $b, (int) $cur['version'], $me);
    ok(['version' => $res['version'] ?? 0, 'restored' => $v]);
}


if (method() === 'GET') {
    ok(read_doc($houseId, $scope));
}

need_post();
need_xhr();
$in = body();
if (!isset($in['body']) || !is_array($in['body'])) fail(400, 'no_body');
$base = (int) ($in['version'] ?? 0);

/* Say what actually went wrong.
 *
 * An unhandled throw here came back as a bare 500 with the reason only in a log
 * on the server, so from the outside "it will not save" was all anybody could
 * tell, on any device, for as long as it lasted. The reason goes back to the
 * person now, because they are the one who can act on it. */
try {
    $res = write_doc($houseId, $scope, $in['body'], $base, $me);
} catch (Throwable $e) {
    error_log('write failed: ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    $msg = $e->getMessage();
    if (strlen($msg) > 200) $msg = substr($msg, 0, 200) . '...';
    send(500, ['ok' => false, 'error' => 'save_failed', 'detail' => $msg]);
}
if (!empty($res['refused'])) {
    send(409, ['ok' => false, 'error' => 'would_wipe',
               'was' => $res['was'], 'now' => $res['now'], 'version' => $res['version']]);
}
if (!empty($res['conflict'])) {
    /* 409 carries the current copy, so the client merges rather than guessing
       or clobbering. */
    send(409, ['ok' => false, 'error' => 'conflict',
               'version' => $res['version'], 'body' => $res['body']]);
}
ok(['version' => $res['version'], '__bv' => $res['__bv'] ?? null, '__dv' => $res['__dv'] ?? null]);
