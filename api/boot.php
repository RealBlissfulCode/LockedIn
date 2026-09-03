<?php
/* Every endpoint starts here. */
declare(strict_types=1);
require __DIR__ . '/lib/http.php';
require __DIR__ . '/lib/db.php';
require __DIR__ . '/lib/google.php';
require __DIR__ . '/lib/auth.php';
require __DIR__ . '/lib/store.php';

if (method() === 'OPTIONS') send(204, []);

/* Never show a stack trace to the browser. It goes in the log. */
set_exception_handler(function (Throwable $e): void {
    error_log('unhandled: ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    fail(500, 'server_error');
});
