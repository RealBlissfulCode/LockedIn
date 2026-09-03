<?php
/* The household: who is in it, inviting somebody, joining, leaving, and the
   people who have a seat but no login yet. */
require __DIR__ . '/boot.php';

$do = $_GET['do'] ?? 'get';

/* Looking up a code has to work before you have an account, because that is
   exactly when you use it. Somebody handed you eight characters and you want
   to know whose household it is before signing in behind it. Nothing here
   leaks anything a person holding the code should not already know. */
if ($do === 'peek') {
    $inv = usable_invite(strtoupper((string) ($_GET['code'] ?? '')));
    if ($inv === null) ok(['valid' => false]);
    $h = one('SELECT name FROM households WHERE id = ?', [(int) $inv['household_id']]);
    ok(['valid' => true, 'household' => $h['name'] ?? '', 'forName' => $inv['display_name']]);
}

$a  = need_account();
$me = (int) $a['id'];

function house_or_404(int $accountId): array {
    $h = my_household($accountId);
    if ($h === null) fail(404, 'no_household');
    return $h;
}
function owner_only(array $h): void {
    if (($h['role'] ?? '') !== 'owner') fail(403, 'owner_only');
}

if ($do === 'get') {
    $h = house_or_404($me);
    ok(['household' => [
        'id' => (int) $h['id'], 'name' => $h['name'], 'plan' => $h['plan'],
        'seats' => (int) $h['seats'], 'used' => seats_used((int) $h['id']),
        'role' => $h['role'], 'memberId' => (int) $h['member_id'],
        'members' => household_members((int) $h['id']),
    ]]);
}

if ($do === 'rename') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    owner_only($h);
    $name = str_field(body(), 'name', 120);
    if ($name === '') fail(400, 'no_name');
    q('UPDATE households SET name = ? WHERE id = ?', [$name, (int) $h['id']]);
    ok(['name' => $name]);
}

/* A seat with nobody in it. This is how you put a partner on the meal plan and
   the schedule before they have signed up, and it is what an invite code
   attaches to when they do. */
if ($do === 'addSeat') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    owner_only($h);
    if (seats_used((int) $h['id']) >= (int) $h['seats']) {
        fail(402, 'no_seats', ['plan' => $h['plan'], 'seats' => (int) $h['seats']]);
    }
    $name = str_field(body(), 'name', 120);
    if ($name === '') fail(400, 'no_name');
    q('INSERT INTO members (household_id, account_id, display_name, role, sort, joined_at)
       VALUES (?, NULL, ?, ?, ?, ?)',
      [(int) $h['id'], $name, 'member', seats_used((int) $h['id']), now()]);
    ok(['members' => household_members((int) $h['id'])]);
}

if ($do === 'renameSeat') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    $in = body();
    $mid = (int) ($in['memberId'] ?? 0);
    $name = str_field($in, 'name', 120);
    if ($name === '') fail(400, 'no_name');
    $row = one('SELECT * FROM members WHERE id = ? AND household_id = ?', [$mid, (int) $h['id']]);
    if ($row === null) fail(404, 'no_member');
    /* You can always rename yourself. Renaming anyone else is the owner's job. */
    if ((int) ($row['account_id'] ?? 0) !== $me) owner_only($h);
    q('UPDATE members SET display_name = ? WHERE id = ?', [$name, $mid]);
    ok(['members' => household_members((int) $h['id'])]);
}

if ($do === 'removeSeat') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    owner_only($h);
    $mid = (int) (body()['memberId'] ?? 0);
    $row = one('SELECT * FROM members WHERE id = ? AND household_id = ?', [$mid, (int) $h['id']]);
    if ($row === null) fail(404, 'no_member');
    if (($row['role'] ?? '') === 'owner') fail(400, 'cannot_remove_owner');
    if ($row['account_id'] !== null) {
        leave_household((int) $row['account_id'], (int) $h['id'], false);
    } else {
        q('DELETE FROM members WHERE id = ?', [$mid]);
    }
    ok(['members' => household_members((int) $h['id'])]);
}

if ($do === 'invite') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    owner_only($h);
    if (seats_used((int) $h['id']) >= (int) $h['seats']) {
        fail(402, 'no_seats', ['plan' => $h['plan'], 'seats' => (int) $h['seats']]);
    }
    $code = new_invite((int) $h['id'], $me, str_field(body(), 'name', 120));
    ok(['code' => $code, 'expiresInDays' => 14]);
}

if ($do === 'invites') {
    $h = house_or_404($me);
    owner_only($h);
    ok(['invites' => all('SELECT code, display_name, created_at, expires_at, used_by, used_at
                            FROM invites
                           WHERE household_id = ? AND revoked_at IS NULL AND used_by IS NULL
                             AND expires_at > ?
                        ORDER BY created_at DESC', [(int) $h['id'], now()])]);
}

if ($do === 'revoke') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    owner_only($h);
    $code = strtoupper(str_field(body(), 'code', 16));
    q('UPDATE invites SET revoked_at = ? WHERE code = ? AND household_id = ?',
      [now(), $code, (int) $h['id']]);
    ok();
}

/* Joining means leaving whatever you were in. If you were the only one left in
   your old household it goes with you, along with everything in it, because
   keeping an empty shell around only makes a mess to clean up later. */
if ($do === 'join') {
    need_post(); need_xhr();
    $in = body();
    $code = strtoupper(str_field($in, 'code', 16));
    $inv = usable_invite($code);
    if ($inv === null) fail(404, 'bad_code');

    $houseId = (int) $inv['household_id'];
    $h = one('SELECT * FROM households WHERE id = ?', [$houseId]);
    if ($h === null) fail(404, 'bad_code');

    $mine = my_household($me);
    if ($mine !== null && (int) $mine['id'] === $houseId) fail(400, 'already_in');
    if (seats_used($houseId) >= (int) $h['seats']) fail(402, 'no_seats');

    $keep = (bool) ($in['keepOld'] ?? false);
    if ($mine !== null) {
        if (($mine['role'] ?? '') === 'owner' && seats_used((int) $mine['id']) > 1) {
            fail(409, 'owner_must_hand_over');
        }
        leave_household($me, (int) $mine['id'], !$keep);
    }

    $db = db();
    $db->beginTransaction();
    try {
        $name = $inv['display_name'] !== '' ? $inv['display_name']
              : ($a['name'] !== '' ? $a['name'] : strtok((string) $a['email'], '@'));
        /* An empty seat left waiting under that name gets claimed rather than
           duplicated, so the plans already written against it carry over. */
        $slot = one('SELECT id FROM members
                      WHERE household_id = ? AND account_id IS NULL AND display_name = ?
                      LIMIT 1', [$houseId, $name]);
        if ($slot !== null) {
            q('UPDATE members SET account_id = ? WHERE id = ?', [$me, (int) $slot['id']]);
        } else {
            q('INSERT INTO members (household_id, account_id, display_name, role, sort, joined_at)
               VALUES (?, ?, ?, ?, ?, ?)',
              [$houseId, $me, $name, 'member', seats_used($houseId), now()]);
        }
        q('UPDATE invites SET used_by = ?, used_at = ? WHERE code = ?', [$me, now(), $code]);
        $db->commit();
    } catch (Throwable $e) {
        $db->rollBack();
        throw $e;
    }
    ok(['household' => household_members($houseId)]);
}

/* Leaving drops your seat and takes your private documents with it. The shared
   document stays behind, because it belongs to the household. */
if ($do === 'leave') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    if (($h['role'] ?? '') === 'owner' && seats_used((int) $h['id']) > 1) {
        fail(409, 'owner_must_hand_over');
    }
    leave_household($me, (int) $h['id'], true);
    create_household($a);
    ok(['household' => my_household($me)]);
}

if ($do === 'handOver') {
    need_post(); need_xhr();
    $h = house_or_404($me);
    owner_only($h);
    $mid = (int) (body()['memberId'] ?? 0);
    $row = one('SELECT * FROM members WHERE id = ? AND household_id = ? AND account_id IS NOT NULL',
               [$mid, (int) $h['id']]);
    if ($row === null) fail(404, 'no_member');
    $db = db();
    $db->beginTransaction();
    try {
        q('UPDATE members SET role = ? WHERE id = ?', ['owner', $mid]);
        q('UPDATE members SET role = ? WHERE household_id = ? AND account_id = ?',
          ['member', (int) $h['id'], $me]);
        q('UPDATE households SET owner_id = ? WHERE id = ?',
          [(int) $row['account_id'], (int) $h['id']]);
        $db->commit();
    } catch (Throwable $e) {
        $db->rollBack();
        throw $e;
    }
    ok(['members' => household_members((int) $h['id'])]);
}

fail(404, 'no_such_action');
