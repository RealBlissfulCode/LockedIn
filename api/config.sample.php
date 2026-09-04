<?php
/* Copy this to config.php and fill it in. config.php is gitignored and must
   never be committed, because it carries the database password.

   On Hostinger: hPanel, Databases, MySQL Databases. Make the database and the
   user, tick all privileges, then paste the four values below. The host is
   almost always localhost even though hPanel shows a longer name. */

return [
    /* Database */
    'db_host' => 'localhost',
    'db_name' => 'lockedin',
    'db_user' => 'lockedin',
    'db_pass' => '',

    /* The OAuth client ID from Google Cloud Console. This one is public, it
       ships in the page. There is no client secret anywhere in this app: the
       browser gets an ID token from Google and the server checks the signature
       against Google's published keys, so there is no secret to leak. */
    'google_client_id' => '417196979541-pact400k1sknkh2tn9ve3js5005hurkk.apps.googleusercontent.com',

    /* Seats per plan. Stripe will move a household between these later. */
    'plans' => [
        'free' => ['seats' => 2],
        'pro'  => ['seats' => 6],
    ],

    /* Set false only on a local http box. Anywhere real this stays true so the
       session cookie is never sent in the clear. */
    'secure_cookies' => true,

    /* Where the cached copy of Google's signing keys lives. Anything writable
       and outside the web root is better; this falls back if it has to. */
    'cache_dir' => null,
];
