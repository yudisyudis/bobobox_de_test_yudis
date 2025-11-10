
SELECT 'Starting Bobobox database setup...' as message;

-- 1. CREATE SCHEMA
SELECT 'Creating schema...' as status;
\i /app/database/schema/00_create_schema.sql

-- 2. CREATE TABLES (URUTAN PENTING!)
SELECT 'Creating tables...' as status;

\i /app/database/schema/01_locations.sql    -- Parent table
\i /app/database/schema/02_guests.sql       -- Parent table  
\i /app/database/schema/03_bookings.sql     -- Child table (butuh locations & guests)
\i /app/database/schema/04_reviews.sql      -- Child table (butuh bookings)

SELECT '✅ All tables created!' as status;

-- 3. INSERT DATA (URUTAN PENTING!)
SELECT 'Inserting sample data...' as status;

\i /app/database/data/01_locations_data.sql    -- Insert parents first
\i /app/database/data/02_guests_data.sql       -- Insert parents first
\i /app/database/data/03_bookings_data.sql     -- Insert children second  
\i /app/database/data/04_reviews_data.sql      -- Insert children last

SELECT '✅ All data inserted!' as status;

-- 4. VERIFICATION
SELECT '🔍 Verifying setup...' as status;

SELECT '📍 Locations: ' || COUNT(*) as count FROM bobobox_test_schema.locations;
SELECT '👥 Guests: ' || COUNT(*) as count FROM bobobox_test_schema.guests;
SELECT '📅 Bookings: ' || COUNT(*) as count FROM bobobox_test_schema.bookings;
SELECT '⭐ Reviews: ' || COUNT(*) as count FROM bobobox_test_schema.reviews;

SELECT '🎉 Bobobox database setup completed!' as message;