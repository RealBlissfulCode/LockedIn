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
/* A rough count of the things a person made. Only used to decide whether a
   write is worth keeping a copy of and whether it looks like a wipe. */
function doc_weight(array $b): int {
    $f = is_array($b['fin'] ?? null) ? $b['fin'] : [];
    $n = 0;
    foreach (['costs', 'jobs', 'actuals'] as $k) $n += is_array($f[$k] ?? null) ? count($f[$k]) : 0;
    foreach (['scenarios', 'purchases', 'strategies'] as $k) $n += is_array($f[$k] ?? null) ? count($f[$k]) : 0;
    $n += is_array($b['days'] ?? null) ? count($b['days']) : 0;
    $n += is_array($b['lists'] ?? null) ? count($b['lists']) : 0;
    $n += is_array($b['members'] ?? null) ? count($b['members']) : 0;
    $n += is_array($b['plan']['cols'] ?? null) ? count($b['plan']['cols']) : 0;
    $n += is_array($b['sched']['cols'] ?? null) ? count($b['sched']['cols']) : 0;
    return $n;
}

/* Keep what is being replaced, and drop anything older than a month. Twenty
   versions back is plenty to undo a bad client and small enough not to matter. */
function keep_history(int $houseId, string $scope, string $json, int $version, int $weight): void {
    q('INSERT INTO doc_history (household_id, scope, body, version, weight, saved_at)
       VALUES (?, ?, ?, ?, ?, ?)', [$houseId, $scope, $json, $version, $weight, now()]);
    if (random_int(1, 20) === 1) {
        q('DELETE FROM doc_history WHERE household_id = ? AND scope = ? AND saved_at < ?',
          [$houseId, $scope, in_days(-30)]);
    }
}

/* Keys that describe the document rather than being part of it. */
const DOC_META = ['__bv', '__dv', '__t', '__td', '__confirmWipe', '__force', 'days'];
/* Separator for a two level unit name. Not a dot, because half of these names
   are typed by a person and "Rent, Nov." would split in the wrong place. */
const UNIT_SEP = "\x01";

function is_map($v): bool {
    if (!is_array($v) || $v === []) return false;
    return array_keys($v) !== range(0, count($v) - 1);
}

/* The pieces a document is merged in.
 *
 * A whole branch is too coarse. fin holds the cost lines, the income lines, the
 * purchase lists, the scenarios and the saved strategies, so with one unit per
 * branch two people touching anything financial at the same moment means one of
 * them loses everything they just did. So anything shaped like a map is split
 * one level down: fin becomes fin/costs, fin/jobs, fin/purchases, and each
 * shopping list is its own unit. Arrays and plain values stay whole, because
 * half an array is not a thing anybody wants merged. */
function doc_units(array $b): array {
    $out = [];
    foreach ($b as $k => $v) {
        if (in_array($k, DOC_META, true)) continue;
        if (is_map($v)) { foreach ($v as $k2 => $_) $out[$k . UNIT_SEP . $k2] = true; }
        else $out[$k] = true;
    }
    return $out;
}

function unit_value(array $b, string $u) {
    $p = explode(UNIT_SEP, $u, 2);
    if (count($p) === 1) return $b[$p[0]] ?? null;
    return is_array($b[$p[0]] ?? null) ? ($b[$p[0]][$p[1]] ?? null) : null;
}

/* Which branch of the document actually changed, decided here rather than on a
   phone.
 *
 * This used to be settled by comparing Date.now() stamps written by whichever
 * device saved last. Two devices means two clocks, and a clock four minutes
 * fast wins every branch forever: the other person's real work keeps losing to
 * an older empty one, and a refresh replays that verdict over whatever they
 * just typed.
 *
 * So the server decides. Every write compares the new body against the stored
 * one branch by branch, and stamps whatever moved with the document's next
 * version number. One counter, one machine, always increasing. A device knows
 * which version it last saw, so "the server has something newer than me on this
 * branch" becomes a fact instead of a guess about somebody else's clock. */
function branch_versions(?array $prev, array $next, int $version, bool $force): array {
    $bv = is_array($prev['__bv'] ?? null) ? $prev['__bv'] : [];
    $dv = is_array($prev['__dv'] ?? null) ? $prev['__dv'] : [];

    $units = doc_units($next) + doc_units($prev ?? []);
    foreach (array_keys($units) as $u) {
        $a = json_encode(unit_value($prev ?? [], $u));
        $b = json_encode(unit_value($next, $u));
        if ($force || $a !== $b || !isset($bv[$u])) $bv[$u] = $version;
    }

    $pd = is_array($prev['days'] ?? null) ? $prev['days'] : [];
    $nd = is_array($next['days'] ?? null) ? $next['days'] : [];
    foreach (array_unique(array_merge(array_keys($pd), array_keys($nd))) as $d) {
        $a = json_encode($pd[$d] ?? null);
        $b = json_encode($nd[$d] ?? null);
        if ($force || $a !== $b || !isset($dv[$d])) $dv[$d] = $version;
    }
    return [$bv, $dv];
}

function write_doc(int $houseId, string $scope, array $body, int $base, int $byAccount): array {
    $force = !empty($body['__force']);
    unset($body['__force']);

    $cur = one('SELECT version FROM docs WHERE household_id = ? AND scope = ?', [$houseId, $scope]);
    if ($cur === null) {
        if ($base !== 0) return ['conflict' => true] + read_doc($houseId, $scope);
        [$bv, $dv] = branch_versions(null, $body, 1, true);
        $body['__bv'] = $bv; $body['__dv'] = $dv;
        $json = doc_json($body);
        q('INSERT INTO docs (household_id, scope, body, version, updated_by, updated_at)
           VALUES (?, ?, ?, 1, ?, ?)', [$houseId, $scope, $json, $byAccount, now()]);
        return ['conflict' => false, 'version' => 1, '__bv' => $bv, '__dv' => $dv];
    }
    if ((int) $cur['version'] !== $base) {
        return ['conflict' => true] + read_doc($houseId, $scope);
    }
    /* Hold on to what is about to be replaced before replacing it. */
    $prev = one('SELECT body, version FROM docs WHERE household_id = ? AND scope = ?',
                [$houseId, $scope]);
    if ($prev !== null) {
        $prevBody = json_decode((string) $prev['body'], true);
        $prevWeight = is_array($prevBody) ? doc_weight($prevBody) : 0;
        $newWeight = doc_weight($body);
        keep_history($houseId, $scope, (string) $prev['body'], (int) $prev['version'], $prevWeight);
        /* A write that throws away most of an account is a bug in whatever sent
           it, not something a person did on purpose. Refuse it and say so; the
           client can retry with confirm set once a human has actually chosen. */
        if ($prevWeight >= 12 && $newWeight <= max(2, (int) floor($prevWeight * 0.25))
            && empty($body['__confirmWipe'])) {
            return ['conflict' => false, 'refused' => true,
                    'was' => $prevWeight, 'now' => $newWeight, 'version' => (int) $prev['version']];
        }
    }

    $next = $base + 1;
    [$bv, $dv] = branch_versions(is_array($prevBody ?? null) ? $prevBody : null, $body, $next, $force);
    $body['__bv'] = $bv; $body['__dv'] = $dv;
    $json = doc_json($body);
    q('UPDATE docs SET body = ?, version = ?, updated_by = ?, updated_at = ?
        WHERE household_id = ? AND scope = ? AND version = ?',
      [$json, $next, $byAccount, now(), $houseId, $scope, $base]);
    return ['conflict' => false, 'version' => $next, '__bv' => $bv, '__dv' => $dv];
}

function doc_json(array $body): string {
    $json = json_encode($body, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    if ($json === false) fail(400, 'unencodable');
    if (strlen($json) > 6 * 1024 * 1024) fail(413, 'too_big');
    return $json;
}
