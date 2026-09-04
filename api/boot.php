<?php
/* Every endpoint starts here. */
declare(strict_types=1);
require __DIR__ . '/lib/http.php';
require __DIR__ . '/lib/db.php';
require __DIR__ . '/lib/google.php';
require __DIR__ . '/lib/auth.php';
require __DIR__ . '/lib/store.php';

/* Shared hosting often ships with display_errors on. One notice printed before
   the JSON and the browser cannot parse the reply, which surfaces as a generic
   "sign in failed" with nothing to go on. Errors go to the log, never the wire. */
@ini_set('display_errors', '0');
@ini_set('log_errors', '1');
error_reporting(E_ALL);
ob_start();

if (method() === 'OPTIONS') send(204, []);

/* Never show a stack trace to the browser. It goes in the log. */
set_exception_handler(function (Throwable $e): void {
    error_log('unhandled: ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    fail(500, 'server_error');
});
