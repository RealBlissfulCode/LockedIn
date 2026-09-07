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

$res = write_doc($houseId, $scope, $in['body'], $base, $me);
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
ok(['version' => $res['version']]);
