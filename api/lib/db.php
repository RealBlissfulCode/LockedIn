<?php
/* One PDO handle, made on first use. Exceptions on, no emulated prepares, so a
   bad query fails loudly in the log instead of quietly returning nothing. */
declare(strict_types=1);

function cfg(): array {
    static $c = null;
    if ($c === null) {
        $path = dirname(__DIR__) . '/config.php';
        if (!is_file($path)) {
            fail(500, 'not_configured');
        }
        $c = require $path;
        if (!is_array($c)) fail(500, 'not_configured');
    }
    return $c;
}

function db(): PDO {
    static $pdo = null;
    if ($pdo !== null) return $pdo;
    $c = cfg();
    $dsn = sprintf('mysql:host=%s;dbname=%s;charset=utf8mb4', $c['db_host'], $c['db_name']);
    try {
        $pdo = new PDO($dsn, $c['db_user'], $c['db_pass'], [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);
    } catch (PDOException $e) {
        error_log('db connect failed: ' . $e->getMessage());
        fail(500, 'db_unavailable');
    }
    return $pdo;
}

function q(string $sql, array $args = []): PDOStatement {
    $st = db()->prepare($sql);
    $st->execute($args);
    return $st;
}

function one(string $sql, array $args = []): ?array {
    $r = q($sql, $args)->fetch();
    return $r === false ? null : $r;
}

function all(string $sql, array $args = []): array {
    return q($sql, $args)->fetchAll();
}

function now(): string {
    return gmdate('Y-m-d H:i:s');
}

function in_days(int $n): string {
    return gmdate('Y-m-d H:i:s', time() + $n * 86400);
}
