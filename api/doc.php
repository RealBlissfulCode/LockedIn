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

if (method() === 'GET') {
    ok(read_doc($houseId, $scope));
}

need_post();
need_xhr();
$in = body();
if (!isset($in['body']) || !is_array($in['body'])) fail(400, 'no_body');
$base = (int) ($in['version'] ?? 0);

$res = write_doc($houseId, $scope, $in['body'], $base, $me);
if (!empty($res['conflict'])) {
    /* 409 carries the current copy, so the client merges rather than guessing
       or clobbering. */
    send(409, ['ok' => false, 'error' => 'conflict',
               'version' => $res['version'], 'body' => $res['body']]);
}
ok(['version' => $res['version']]);
