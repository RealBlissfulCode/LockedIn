<?php
/* Bringing the old handbook data across.
 *
 * Before accounts existed the whole household lived in one state.json written
 * by the old sync endpoint, either above the web root or in api/data. That file
 * is still sitting there after the rewrite, and it is the only copy that was
 * never tied to one browser.
 *
 * This hands it back to the signed in owner so the app can migrate it and push
 * it up as their household's document. It never writes anything itself, and it
 * only ever answers the person who owns the household.
 */
require __DIR__ . '/boot.php';

$a = need_account();
$me = (int) $a['id'];
$h = my_household($me);
if ($h === null) fail(404, 'no_household');
if (($h['role'] ?? '') !== 'owner') fail(403, 'owner_only');

/* Both places the old endpoint could have chosen, in the order it chose them. */
function legacy_paths(): array {
    return [
        dirname(__DIR__, 2) . '/handbook-data/state.json',
        dirname(__DIR__, 2) . '/lockedin-data/state.json',
        __DIR__ . '/data/state.json',
    ];
}

function legacy_file(): ?string {
    foreach (legacy_paths() as $p) {
        if (is_file($p) && is_readable($p) && filesize($p) > 40) return $p;
    }
    return null;
}

$do = $_GET['do'] ?? 'peek';
$file = legacy_file();

if ($do === 'peek') {
    if ($file === null) ok(['found' => false]);
    $raw = (string) file_get_contents($file);
    $j = json_decode($raw, true);
    $st = is_array($j) ? ($j['state'] ?? null) : null;
    if (!is_array($st)) ok(['found' => false]);
    /* Enough to recognise it as yours without handing any of it over yet. */
    ok(['found' => true,
        'updatedAt' => $j['updatedAt'] ?? null,
        'version'   => (int) ($j['version'] ?? 0),
        'counts'    => [
            'costs'      => count($st['fin']['costs'] ?? []),
            'jobs'       => count($st['fin']['jobs'] ?? []),
            'scenarios'  => count($st['fin']['scenarios'] ?? []),
            'days'       => count($st['days'] ?? []),
            'lists'      => count($st['lists'] ?? []),
            'plans'      => count($st['plan']['cols'] ?? []),
            'schedules'  => count($st['sched']['cols'] ?? []),
        ]]);
}

/* The household's original data, rebuilt out of the files the product rewrite
   deleted. Shipped with the app so restoring it is a button rather than a file
   somebody has to be sent, and served only to a signed in household owner. */
if ($do === 'seed') {
    $p = __DIR__ . '/seed-restore.php';
    if (!is_file($p)) ok(['found' => false]);
    $j = require $p;
    $st = is_array($j) ? ($j['state'] ?? null) : null;
    if (!is_array($st)) ok(['found' => false]);
    ok(['found' => true, 'state' => $st,
        'counts' => [
            'costs' => count($st['fin']['costs'] ?? []),
            'jobs' => count($st['fin']['jobs'] ?? []),
            'purchases' => count($st['fin']['purchases'] ?? []),
            'strategies' => count($st['fin']['strategies'] ?? []),
            'plans' => count($st['plan']['cols'] ?? []),
        ]]);
}

if ($do === 'fetch') {
    need_post();
    need_xhr();
    if ($file === null) fail(404, 'nothing_to_import');
    $j = json_decode((string) file_get_contents($file), true);
    $st = is_array($j) ? ($j['state'] ?? null) : null;
    if (!is_array($st)) fail(422, 'unreadable');
    ok(['state' => $st, 'updatedAt' => $j['updatedAt'] ?? null]);
}

fail(404, 'no_such_action');
