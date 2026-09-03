<?php
/* Sign in, sign out, and who am I.
 *
 * The browser hands us the ID token Google gave it. We check the signature,
 * then either find the account by its Google subject id or make one. First
 * time through, the account gets a household of one with nothing in it. */
require __DIR__ . '/boot.php';

$do = $_GET['do'] ?? 'me';

if ($do === 'me') {
    $a = current_account();
    if ($a === null) ok(['signedIn' => false, 'clientId' => (string) (cfg()['google_client_id'] ?? '')]);
    $h = my_household((int) $a['id']);
    ok([
        'signedIn'  => true,
        'account'   => ['id' => (int) $a['id'], 'email' => $a['email'], 'name' => $a['name'],
                        'avatar' => $a['avatar'], 'onboarded' => (bool) $a['onboarded']],
        'household' => $h === null ? null : [
            'id' => (int) $h['id'], 'name' => $h['name'], 'plan' => $h['plan'],
            'seats' => (int) $h['seats'], 'used' => seats_used((int) $h['id']),
            'role' => $h['role'], 'memberId' => (int) $h['member_id'],
            'members' => household_members((int) $h['id']),
        ],
    ]);
}

if ($do === 'google') {
    need_post();
    need_xhr();
    $in = body();
    $tok = str_field($in, 'credential', 4096);
    if ($tok === '') fail(400, 'no_credential');

    $claims = verify_google_token($tok, (string) (cfg()['google_client_id'] ?? ''));
    if ($claims === null) fail(401, 'bad_token');

    $sub   = (string) $claims['sub'];
    $email = strtolower((string) $claims['email']);
    $name  = trim((string) ($claims['name'] ?? ''));
    $pic   = (string) ($claims['picture'] ?? '');

    $acct = one('SELECT * FROM accounts WHERE google_sub = ?', [$sub]);
    if ($acct === null) {
        /* Same person, new Google subject id, is not a thing that happens. An
           email match with a different sub means somebody re-registered the
           address, so the old row keeps its data and this one is refused
           rather than quietly handed the wrong household. */
        $clash = one('SELECT id FROM accounts WHERE email = ?', [$email]);
        if ($clash !== null) fail(409, 'email_in_use');

        q('INSERT INTO accounts (google_sub, email, name, avatar, created_at, last_seen_at)
           VALUES (?, ?, ?, ?, ?, ?)', [$sub, $email, $name, $pic, now(), now()]);
        $acct = one('SELECT * FROM accounts WHERE google_sub = ?', [$sub]);
        $fresh = true;
    } else {
        /* Keep the display bits current, leave everything else alone. */
        q('UPDATE accounts SET email = ?, name = ?, avatar = ?, last_seen_at = ? WHERE id = ?',
          [$email, $name !== '' ? $name : $acct['name'], $pic, now(), (int) $acct['id']]);
        $acct['email'] = $email;
        if ($name !== '') $acct['name'] = $name;
        $acct['avatar'] = $pic;
        $fresh = false;
    }

    if (my_household((int) $acct['id']) === null) {
        create_household($acct);
    }

    start_session((int) $acct['id']);
    sweep_expired();
    ok(['fresh' => $fresh, 'onboarded' => (bool) $acct['onboarded']]);
}

if ($do === 'out') {
    need_post();
    need_xhr();
    end_session();
    ok();
}

if ($do === 'onboarded') {
    need_post();
    need_xhr();
    $a = need_account();
    q('UPDATE accounts SET onboarded = 1 WHERE id = ?', [(int) $a['id']]);
    ok();
}

fail(404, 'no_such_action');
