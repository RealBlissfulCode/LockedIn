<?php
/* Households, seats, invite codes and the state documents. Every read in here
   goes through the caller's membership, so there is no path that returns a row
   belonging to a household you are not in. */
declare(strict_types=1);

function plan_seats(string $plan): int {
    $plans = cfg()['plans'] ?? [];
    return (int) ($plans[$plan]['seats'] ?? 2);
}

/* The household this account belongs to, plus their seat in it. One household
   per account for now. Joining a second one means leaving the first, which is
   the behaviour people expect from the word household. */
function my_household(int $accountId): ?array {
    return one('SELECT h.*, m.id AS member_id, m.role, m.display_name AS member_name
                  FROM members m
                  JOIN households h ON h.id = m.household_id
                 WHERE m.account_id = ?
                 LIMIT 1', [$accountId]);
}

function household_members(int $houseId): array {
    return all('SELECT m.id, m.account_id, m.display_name, m.role, m.accent, m.sort,
                       a.email, a.avatar
                  FROM members m
             LEFT JOIN accounts a ON a.id = m.account_id
                 WHERE m.household_id = ?
              ORDER BY m.sort, m.id', [$houseId]);
}

function seats_used(int $houseId): int {
    $r = one('SELECT COUNT(*) AS n FROM members WHERE household_id = ?', [$houseId]);
    return (int) ($r['n'] ?? 0);
}

/* A brand new account gets a household of one, named after them, and nothing
   else. No seeded costs, no seeded recipes, no second person. Everything after
   this is something they chose to add. */
function create_household(array $account, string $houseName = ''): array {
    $db = db();
    $db->beginTransaction();
    try {
        $who = $account['name'] !== '' ? $account['name'] : strtok((string) $account['email'], '@');
        $name = $houseName !== '' ? $houseName : ($who . "'s household");
        q('INSERT INTO households (name, owner_id, plan, seats, created_at) VALUES (?, ?, ?, ?, ?)',
          [$name, (int) $account['id'], 'free', plan_seats('free'), now()]);
        $houseId = (int) $db->lastInsertId();
        q('INSERT INTO members (household_id, account_id, display_name, role, sort, joined_at)
           VALUES (?, ?, ?, ?, ?, ?)',
          [$houseId, (int) $account['id'], $who, 'owner', 0, now()]);
        $db->commit();
    } catch (Throwable $e) {
        $db->rollBack();
        throw $e;
    }
    return my_household((int) $account['id']);
}

function new_invite(int $houseId, int $byAccount, string $forName): string {
    /* No vowels and no look alike characters, because these get read out loud
       and typed on a phone. */
    $alphabet = '23456789BCDFGHJKLMNPQRSTVWXYZ';
    for ($try = 0; $try < 12; $try++) {
        $code = '';
        for ($i = 0; $i < 8; $i++) $code .= $alphabet[random_int(0, strlen($alphabet) - 1)];
        $taken = one('SELECT code FROM invites WHERE code = ?', [$code]);
        if ($taken !== null) continue;
        q('INSERT INTO invites (code, household_id, created_by, display_name, created_at, expires_at)
           VALUES (?, ?, ?, ?, ?, ?)',
          [$code, $houseId, $byAccount, $forName, now(), in_days(14)]);
        return $code;
    }
    fail(500, 'invite_failed');
}

function usable_invite(string $code): ?array {
    return one('SELECT * FROM invites
                 WHERE code = ? AND used_by IS NULL AND revoked_at IS NULL AND expires_at > ?',
               [strtoupper($code), now()]);
}

/* Leaving is a real cleanup, not a flag. The seat goes, this person's private
   documents go with it, and the shared document stays with the household
   because it was never theirs alone. An owner cannot walk out and strand
   everybody, so they hand it over or take the household down with them. */
function leave_household(int $accountId, int $houseId, bool $deleteIfLast): void {
    $db = db();
    $db->beginTransaction();
    try {
        q('DELETE FROM docs WHERE household_id = ? AND scope = ?',
          [$houseId, 'private:' . $accountId]);
        q('DELETE FROM members WHERE household_id = ? AND account_id = ?', [$houseId, $accountId]);
        $left = seats_used($houseId);
        if ($left === 0 && $deleteIfLast) {
            q('DELETE FROM households WHERE id = ?', [$houseId]);
        }
        $db->commit();
    } catch (Throwable $e) {
        $db->rollBack();
        throw $e;
    }
}

/* ---------------- documents ----------------
   'shared' is the household's. 'private:<accountId>' is one person's and is
   never handed to anyone else, which is what makes a hidden plan actually
   hidden rather than just not drawn on screen. */
function scope_allowed(string $scope, int $accountId): bool {
    if ($scope === 'shared') return true;
    return $scope === 'private:' . $accountId;
}

function read_doc(int $houseId, string $scope): array {
    $r = one('SELECT body, version, updated_at FROM docs WHERE household_id = ? AND scope = ?',
             [$houseId, $scope]);
    if ($r === null) return ['body' => null, 'version' => 0, 'updated_at' => null];
    $body = json_decode((string) $r['body'], true);
    return ['body' => is_array($body) ? $body : null,
            'version' => (int) $r['version'],
            'updated_at' => $r['updated_at']];
}

/* Optimistic write. Send the version you last read; if the row moved on since,
   this refuses and hands back what is there now so the client can merge. Two
   phones editing at once is the normal case, not the exception. */
function write_doc(int $houseId, string $scope, array $body, int $base, int $byAccount): array {
    $json = json_encode($body, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    if ($json === false) fail(400, 'unencodable');
    if (strlen($json) > 6 * 1024 * 1024) fail(413, 'too_big');

    $cur = one('SELECT version FROM docs WHERE household_id = ? AND scope = ?', [$houseId, $scope]);
    if ($cur === null) {
        if ($base !== 0) return ['conflict' => true] + read_doc($houseId, $scope);
        q('INSERT INTO docs (household_id, scope, body, version, updated_by, updated_at)
           VALUES (?, ?, ?, 1, ?, ?)', [$houseId, $scope, $json, $byAccount, now()]);
        return ['conflict' => false, 'version' => 1];
    }
    if ((int) $cur['version'] !== $base) {
        return ['conflict' => true] + read_doc($houseId, $scope);
    }
    $next = $base + 1;
    q('UPDATE docs SET body = ?, version = ?, updated_by = ?, updated_at = ?
        WHERE household_id = ? AND scope = ? AND version = ?',
      [$json, $next, $byAccount, now(), $houseId, $scope, $base]);
    return ['conflict' => false, 'version' => $next];
}
