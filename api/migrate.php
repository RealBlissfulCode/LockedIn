<?php
/* Creates the tables. Run it once after filling in config.php:
 *
 *     php api/migrate.php
 *
 * Over the web it needs ?key= matching a one time file you drop next to it,
 * because Hostinger shared plans do not all give you shell access. Make the
 * file, hit the url, delete the file.
 */
declare(strict_types=1);

$cli = PHP_SAPI === 'cli';
require __DIR__ . '/lib/http.php';
require __DIR__ . '/lib/db.php';

if (!$cli) {
    $keyFile = __DIR__ . '/.migrate-key';
    if (!is_file($keyFile)) fail(403, 'no_key_file');
    $want = trim((string) file_get_contents($keyFile));
    $got  = (string) ($_GET['key'] ?? '');
    if ($want === '' || !hash_equals($want, $got)) fail(403, 'bad_key');
}

/* Drop the comment lines before splitting, not after. Every table in the file
   has a comment block above it, so splitting first and then skipping anything
   that opens with a dash throws away the statement attached to it. */
$sql = (string) file_get_contents(__DIR__ . '/schema.sql');
$lines = [];
foreach (explode("\n", $sql) as $line) {
    if (str_starts_with(ltrim($line), '--')) continue;
    $lines[] = $line;
}
$done = [];
foreach (array_filter(array_map('trim', explode(';', implode("\n", $lines)))) as $stmt) {
    if ($stmt === '') continue;
    db()->exec($stmt);
    if (preg_match('/CREATE TABLE IF NOT EXISTS\s+`?(\w+)`?/i', $stmt, $m)) $done[] = $m[1];
}

if ($cli) {
    echo "tables ready: " . implode(', ', $done) . "\n";
    exit(0);
}
ok(['tables' => $done]);
