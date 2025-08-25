DROP TABLE IF EXISTS builds CASCADE;

CREATE TABLE builds (
    github_run_id BIGINT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    repo TEXT NOT NULL,
    branch TEXT NOT NULL,
    status TEXT NOT NULL, -- success, failure, in_progress
    finished_at TIMESTAMPTZ,
    duration_seconds FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (github_run_id, started_at)
);

-- Convert to hypertable for TimescaleDB
SELECT create_hypertable('builds', 'started_at', if_not_exists => TRUE);
 