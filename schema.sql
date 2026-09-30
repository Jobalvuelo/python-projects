CREATE TABLE IF NOT EXISTS bookings (
  id TEXT PRIMARY KEY,
  package_key TEXT NOT NULL,
  arrival_date TEXT NOT NULL,
  guests INTEGER NOT NULL CHECK (guests BETWEEN 1 AND 6),
  guest_name TEXT NOT NULL,
  guest_email TEXT NOT NULL,
  message TEXT,
  status TEXT NOT NULL DEFAULT 'pending',
  stripe_session_id TEXT UNIQUE,
  stripe_payment_intent_id TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_bookings_arrival ON bookings(arrival_date);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
