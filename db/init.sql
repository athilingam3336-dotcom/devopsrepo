-- Runs once when the PostgreSQL container is first created.
-- SQLAlchemy creates the actual tables; this file seeds sample data.

-- Wait for the table (created by SQLAlchemy on first backend boot).
-- We use a DO block so the script is safe to run at init time.
DO $$
BEGIN
  -- Only seed if the table already exists
  IF EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'data_entries'
  ) THEN
    INSERT INTO data_entries (name, message, created_at) VALUES
      ('Alice',   'Hello from the seed file!',  NOW()),
      ('Bob',     'PostgreSQL is running 🐘',   NOW()),
      ('Charlie', 'Docker Compose works!',       NOW())
    ON CONFLICT DO NOTHING;
  END IF;
END $$;
