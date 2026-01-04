-- Full DB schema

-- Centres table
CREATE TABLE IF NOT EXISTS centres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    district TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Date-wise summaries table
CREATE TABLE IF NOT EXISTS datewise_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    centre_id INTEGER NOT NULL,
    date DATE NOT NULL,
    farmer_count INTEGER NOT NULL,
    quantity REAL NOT NULL,
    amount REAL NOT NULL,
    details_url TEXT,
    data_state TEXT DEFAULT 'OPEN',  -- OPEN, CLOSING, CLOSED
    last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    html_hash TEXT,
    FOREIGN KEY (centre_id) REFERENCES centres (id),
    UNIQUE(centre_id, date)
);

-- Farmer transaction details table
CREATE TABLE IF NOT EXISTS farmer_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    centre_id INTEGER NOT NULL,
    date DATE NOT NULL,
    farmer_id TEXT,
    farmer_name TEXT,
    village TEXT,
    quantity REAL,
    amount REAL,
    transaction_time TEXT,
    last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (centre_id) REFERENCES centres (id)
    -- Removed UNIQUE constraint as same farmer can have multiple transactions on same day
);

-- Activity logs table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    component TEXT NOT NULL,
    level TEXT NOT NULL,  -- INFO, WARNING, ERROR
    message TEXT NOT NULL,
    details TEXT
);

-- Pre-aggregated statistics table
CREATE TABLE IF NOT EXISTS aggregated_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_type TEXT NOT NULL,  -- daily, centre, global
    date DATE,
    centre_id INTEGER,
    farmer_count INTEGER,
    quantity REAL,
    amount REAL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (centre_id) REFERENCES centres (id)
);

-- Sync state tracking table
CREATE TABLE IF NOT EXISTS sync_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    centre_id INTEGER,
    date DATE,
    state TEXT NOT NULL,  -- OPEN, CLOSING, CLOSED
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (centre_id) REFERENCES centres (id),
    UNIQUE(centre_id, date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_centres_name ON centres(name);
CREATE INDEX IF NOT EXISTS idx_datewise_centre_date ON datewise_summaries(centre_id, date);
CREATE INDEX IF NOT EXISTS idx_farmer_centre_date ON farmer_transactions(centre_id, date);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_sync_state_centre_date ON sync_state(centre_id, date);