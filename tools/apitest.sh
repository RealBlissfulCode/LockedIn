#!/bin/bash
# End to end pass over the API. Real HTTP, real cookies, real signed tokens.
#
# It never talks to Google. tools/fakegoogle.php makes a keypair, drops the
# public half where the app caches Google's signing keys, and mints tokens with
# it, so the signature checking and the claim checks all get exercised for real.
#
#   php api/migrate.php
#   php -S 127.0.0.1:8080 -t .
#   tools/apitest.sh
B=${API:-http://127.0.0.1:8080/api}
PASS=0; FAIL=0
ck(){ if [ "$2" = "$3" ]; then echo "PASS $1"; PASS=$((PASS+1));
      else echo "FAIL $1 :: got [$2] want [$3]"; FAIL=$((FAIL+1)); fi }
ckhas(){ if echo "$2" | grep -q "$3"; then echo "PASS $1"; PASS=$((PASS+1));
      else echo "FAIL $1 :: [$2] lacks [$3]"; FAIL=$((FAIL+1)); fi }
J='-H Content-Type:application/json -H X-LockedIn:1'
signin(){ # $1 cookiejar  $2 token
  curl -s -c "$1" -b "$1" $J -X POST "$B/auth.php?do=google" -d "{\"credential\":\"$2\"}"; }

rm -f /tmp/c1 /tmp/c2 /tmp/c3

echo "--- token verification ---"
T=$(php /tmp/mkjwt.php '{}')
ckhas "valid token signs in"        "$(signin /tmp/c1 "$T")" '"ok":true'
BAD=$(php /tmp/mkjwt.php '{"__breaksig":true}')
ckhas "tampered signature refused"  "$(signin /tmp/cx "$BAD")" 'bad_token'
BAD=$(php /tmp/mkjwt.php '{"aud":"someone-elses-app.apps.googleusercontent.com"}')
ckhas "wrong audience refused"      "$(signin /tmp/cx "$BAD")" 'bad_token'
BAD=$(php /tmp/mkjwt.php '{"exp":1000000000,"iat":999999000}')
ckhas "expired token refused"       "$(signin /tmp/cx "$BAD")" 'bad_token'
BAD=$(php /tmp/mkjwt.php '{"email_verified":false,"sub":"22","email":"x@y.com"}')
ckhas "unverified email refused"    "$(signin /tmp/cx "$BAD")" 'bad_token'
BAD=$(php /tmp/mkjwt.php '{"iss":"https://evil.example","sub":"33","email":"z@y.com"}')
ckhas "wrong issuer refused"        "$(signin /tmp/cx "$BAD")" 'bad_token'
BAD=$(php /tmp/mkjwt.php '{"__kid":"unknown-kid","sub":"44","email":"q@y.com"}')
ckhas "unknown key id refused"      "$(signin /tmp/cx "$BAD")" 'bad_token'

echo "--- csrf and method guards ---"
ckhas "state change needs header"   "$(curl -s -X POST "$B/auth.php?do=google" -d '{}')" 'bad_origin'
ckhas "signed out is 401"           "$(curl -s "$B/household.php?do=get")" 'signed_out'

echo "--- account and household ---"
ME=$(curl -s -b /tmp/c1 "$B/auth.php?do=me")
ckhas "session sticks"              "$ME" '"signedIn":true'
ckhas "email captured"              "$ME" 'jaronnorris7@gmail.com'
ckhas "household auto created"      "$ME" '"role":"owner"'
ckhas "free plan"                   "$ME" '"plan":"free"'
ckhas "two seats on free"           "$ME" '"seats":2'
ckhas "one seat used"               "$ME" '"used":1'
ckhas "starts un-onboarded"         "$ME" '"onboarded":false'

echo "--- documents ---"
ckhas "doc starts empty"            "$(curl -s -b /tmp/c1 "$B/doc.php?scope=shared")" '"version":0'
W=$(curl -s -b /tmp/c1 $J -X POST "$B/doc.php?scope=shared" -d '{"version":0,"body":{"fin":{"jobs":[]}}}')
ckhas "first write lands at v1"     "$W" '"version":1'
W=$(curl -s -b /tmp/c1 $J -X POST "$B/doc.php?scope=shared" -d '{"version":1,"body":{"fin":{"jobs":[1]}}}')
ckhas "second write lands at v2"    "$W" '"version":2'
W=$(curl -s -b /tmp/c1 $J -X POST "$B/doc.php?scope=shared" -d '{"version":1,"body":{"fin":"stale"}}')
ckhas "stale write conflicts"       "$W" '"error":"conflict"'
ckhas "conflict returns current"    "$W" '"jobs":\[1\]'
ckhas "private scope of mine ok"    "$(curl -s -b /tmp/c1 "$B/doc.php?scope=private:1")" '"version":0'
ckhas "private scope of others no"  "$(curl -s -b /tmp/c1 "$B/doc.php?scope=private:999")" 'bad_scope'
ckhas "read all works"              "$(curl -s -b /tmp/c1 "$B/doc.php?do=all")" '"shared"'

echo "--- invites and joining ---"
INV=$(curl -s -b /tmp/c1 $J -X POST "$B/household.php?do=invite" -d '{"name":"Aaliyah"}')
CODE=$(echo "$INV" | sed -n 's/.*"code":"\([A-Z0-9]*\)".*/\1/p')
ck   "invite code is 8 chars"       "${#CODE}" "8"
ckhas "peek names the household"    "$(curl -s "$B/household.php?do=peek&code=$CODE")" '"valid":true'
ckhas "peek on junk is invalid"     "$(curl -s "$B/household.php?do=peek&code=ZZZZZZZZ")" '"valid":false'

T2=$(php /tmp/mkjwt.php '{"sub":"220000000000000000002","email":"partner@example.com","name":"Aaliyah"}')
ckhas "second account signs in"     "$(signin /tmp/c2 "$T2")" '"ok":true'
ckhas "joining with the code works" "$(curl -s -b /tmp/c2 $J -X POST "$B/household.php?do=join" -d "{\"code\":\"$CODE\"}")" '"ok":true'
ckhas "code cannot be reused"       "$(curl -s "$B/household.php?do=peek&code=$CODE")" '"valid":false'
H=$(curl -s -b /tmp/c1 "$B/household.php?do=get")
ckhas "two seats used now"          "$H" '"used":2'
ckhas "partner is listed"           "$H" 'partner@example.com'
ckhas "partner is not owner"        "$(curl -s -b /tmp/c2 "$B/household.php?do=get")" '"role":"member"'

echo "--- shared data really is shared ---"
ckhas "partner sees shared doc"     "$(curl -s -b /tmp/c2 "$B/doc.php?scope=shared")" '"jobs":\[1\]'
curl -s -b /tmp/c2 $J -X POST "$B/doc.php?scope=private:2" -d '{"version":0,"body":{"secret":"gift"}}' >/dev/null
ckhas "partner private is private"  "$(curl -s -b /tmp/c1 "$B/doc.php?scope=private:2")" 'bad_scope'
ckhas "owner private stays empty"   "$(curl -s -b /tmp/c1 "$B/doc.php?do=all")" '"private":{"body":null'

echo "--- seat limits ---"
ckhas "free plan blocks a 3rd seat" "$(curl -s -b /tmp/c1 $J -X POST "$B/household.php?do=invite" -d '{"name":"Third"}')" 'no_seats'
ckhas "member cannot invite"        "$(curl -s -b /tmp/c2 $J -X POST "$B/household.php?do=invite" -d '{"name":"X"}')" 'owner_only'
ckhas "owner with others cant bail" "$(curl -s -b /tmp/c1 $J -X POST "$B/household.php?do=leave" -d '{}')" 'owner_must_hand_over'

echo "--- leaving cleans up ---"
ckhas "member can leave"            "$(curl -s -b /tmp/c2 $J -X POST "$B/household.php?do=leave" -d '{}')" '"ok":true'
ckhas "leaver gets a fresh house"   "$(curl -s -b /tmp/c2 "$B/household.php?do=get")" '"used":1'
ckhas "leaver sees no old data"     "$(curl -s -b /tmp/c2 "$B/doc.php?scope=shared")" '"version":0'
ckhas "seat freed for the owner"    "$(curl -s -b /tmp/c1 "$B/household.php?do=get")" '"used":1'
ckhas "owner data untouched"        "$(curl -s -b /tmp/c1 "$B/doc.php?scope=shared")" '"jobs":\[1\]'

echo "--- sign out ---"
ckhas "sign out works"              "$(curl -s -b /tmp/c1 -c /tmp/c1 $J -X POST "$B/auth.php?do=out")" '"ok":true'
ckhas "cookie is dead after"        "$(curl -s -b /tmp/c1 "$B/household.php?do=get")" 'signed_out'

echo
echo "passed $PASS, failed $FAIL"
[ "$FAIL" = "0" ]
