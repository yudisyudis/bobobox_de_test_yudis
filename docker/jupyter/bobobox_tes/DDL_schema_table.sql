-- DROP SCHEMA "BOBOBOX_TEST_SQL_SCHEMA";

CREATE SCHEMA "BOBOBOX_TEST_SQL_SCHEMA" AUTHORIZATION postgres;
-- "BOBOBOX_TEST_SQL_SCHEMA".guests definition

-- Drop table

-- DROP TABLE "BOBOBOX_TEST_SQL_SCHEMA".guests;

CREATE TABLE "BOBOBOX_TEST_SQL_SCHEMA".guests (
	guest_id varchar(10) NOT NULL,
	guest_name varchar(100) NOT NULL,
	registration_date date NOT NULL,
	CONSTRAINT guests_pkey PRIMARY KEY (guest_id)
);


-- "BOBOBOX_TEST_SQL_SCHEMA".locations definition

-- Drop table

-- DROP TABLE "BOBOBOX_TEST_SQL_SCHEMA".locations;

CREATE TABLE "BOBOBOX_TEST_SQL_SCHEMA".locations (
	location_id varchar(10) NOT NULL,
	location_name varchar(100) NOT NULL,
	city varchar(50) NOT NULL,
	"type" varchar(10) NULL,
	total_units int4 NOT NULL,
	CONSTRAINT locations_pkey PRIMARY KEY (location_id),
	CONSTRAINT locations_type_check CHECK (((type)::text = ANY ((ARRAY['Pod'::character varying, 'Cabin'::character varying])::text[])))
);


-- "BOBOBOX_TEST_SQL_SCHEMA".bookings definition

-- Drop table

-- DROP TABLE "BOBOBOX_TEST_SQL_SCHEMA".bookings;

CREATE TABLE "BOBOBOX_TEST_SQL_SCHEMA".bookings (
	booking_id varchar(10) NOT NULL,
	guest_id varchar(10) NOT NULL,
	location_id varchar(10) NOT NULL,
	booking_date date NOT NULL,
	check_in_date date NOT NULL,
	duration int4 NOT NULL,
	total_price numeric(10, 2) NOT NULL,
	CONSTRAINT bookings_duration_check CHECK ((duration >= 0)),
	CONSTRAINT bookings_pkey PRIMARY KEY (booking_id),
	CONSTRAINT bookings_guest_id_fkey FOREIGN KEY (guest_id) REFERENCES "BOBOBOX_TEST_SQL_SCHEMA".guests(guest_id),
	CONSTRAINT bookings_location_id_fkey FOREIGN KEY (location_id) REFERENCES "BOBOBOX_TEST_SQL_SCHEMA".locations(location_id)
);


-- "BOBOBOX_TEST_SQL_SCHEMA".reviews definition

-- Drop table

-- DROP TABLE "BOBOBOX_TEST_SQL_SCHEMA".reviews;

CREATE TABLE "BOBOBOX_TEST_SQL_SCHEMA".reviews (
	review_id varchar(10) NOT NULL,
	booking_id varchar(10) NOT NULL,
	rating int4 NOT NULL,
	"comment" text NULL,
	review_date date NOT NULL,
	CONSTRAINT reviews_pkey PRIMARY KEY (review_id),
	CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
	CONSTRAINT reviews_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES "BOBOBOX_TEST_SQL_SCHEMA".bookings(booking_id)
);