-- LockedIn database. Run it with: php api/migrate.php
--
-- Everything hangs off a household. An account is a person who can log in, a
-- member is that person's seat in a household, and the state documents belong
-- to the household rather than to any one person. That way handing the app to
-- a partner is adding a seat, not copying data around.
--
-- utf8mb4 throughout because people put emoji in list names.

CREATE TABLE IF NOT EXISTS accounts (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  google_sub    VARCHAR(64)     NOT NULL,
  email         VARCHAR(255)    NOT NULL,
  name          VARCHAR(120)    NOT NULL DEFAULT '',
  avatar        VARCHAR(512)    NOT NULL DEFAULT '',
  onboarded     TINYINT(1)      NOT NULL DEFAULT 0,
  created_at    DATETIME        NOT NULL,
  last_seen_at  DATETIME        NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_google_sub (google_sub),
  UNIQUE KEY uq_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- plan lives on the household, not the person, so one subscription covers
-- everyone under it. seats is denormalised from the plan on purpose: changing
-- what a tier is worth later should not silently resize existing households.
CREATE TABLE IF NOT EXISTS households (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name          VARCHAR(120)    NOT NULL DEFAULT 'My household',
  owner_id      BIGINT UNSIGNED NOT NULL,
  plan          VARCHAR(16)     NOT NULL DEFAULT 'free',
  seats         SMALLINT        NOT NULL DEFAULT 2,
  created_at    DATETIME        NOT NULL,
  PRIMARY KEY (id),
  KEY ix_owner (owner_id),
  CONSTRAINT fk_house_owner FOREIGN KEY (owner_id) REFERENCES accounts (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- A member can exist with no account attached. That is how you put someone on
-- the meal plan and the schedule before they have ever signed in, and how a
-- seat survives that person leaving.
CREATE TABLE IF NOT EXISTS members (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  household_id  BIGINT UNSIGNED NOT NULL,
  account_id    BIGINT UNSIGNED NULL,
  display_name  VARCHAR(120)    NOT NULL,
  role          VARCHAR(16)     NOT NULL DEFAULT 'member',
  accent        VARCHAR(16)     NOT NULL DEFAULT '',
  sort          SMALLINT        NOT NULL DEFAULT 0,
  joined_at     DATETIME        NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_house_account (household_id, account_id),
  KEY ix_house (household_id),
  CONSTRAINT fk_member_house FOREIGN KEY (household_id) REFERENCES households (id) ON DELETE CASCADE,
  CONSTRAINT fk_member_account FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS invites (
  code          VARCHAR(16)     NOT NULL,
  household_id  BIGINT UNSIGNED NOT NULL,
  created_by    BIGINT UNSIGNED NOT NULL,
  display_name  VARCHAR(120)    NOT NULL DEFAULT '',
  created_at    DATETIME        NOT NULL,
  expires_at    DATETIME        NOT NULL,
  used_by       BIGINT UNSIGNED NULL,
  used_at       DATETIME        NULL,
  revoked_at    DATETIME        NULL,
  PRIMARY KEY (code),
  KEY ix_house (household_id),
  CONSTRAINT fk_invite_house FOREIGN KEY (household_id) REFERENCES households (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- One row per document. scope 'shared' is what everyone in the household sees.
-- scope 'private:<accountId>' is that person's own, and the server never hands
-- it to anybody else, which is what makes hiding a surprise actually hidden
-- rather than just not drawn.
CREATE TABLE IF NOT EXISTS docs (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  household_id  BIGINT UNSIGNED NOT NULL,
  scope         VARCHAR(48)     NOT NULL,
  body          LONGTEXT        NOT NULL,
  version       BIGINT UNSIGNED NOT NULL DEFAULT 1,
  updated_by    BIGINT UNSIGNED NULL,
  updated_at    DATETIME        NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_house_scope (household_id, scope),
  CONSTRAINT fk_doc_house FOREIGN KEY (household_id) REFERENCES households (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Session tokens are stored hashed. A dump of this table does not let anybody
-- log in as anyone.
CREATE TABLE IF NOT EXISTS sessions (
  token_hash    CHAR(64)        NOT NULL,
  account_id    BIGINT UNSIGNED NOT NULL,
  created_at    DATETIME        NOT NULL,
  expires_at    DATETIME        NOT NULL,
  seen_at       DATETIME        NOT NULL,
  ua            VARCHAR(255)    NOT NULL DEFAULT '',
  PRIMARY KEY (token_hash),
  KEY ix_account (account_id),
  KEY ix_expires (expires_at),
  CONSTRAINT fk_sess_account FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
