CREATE TABLE bobobox_test_schema.bookings (
	booking_id varchar(10) NOT NULL,
	guest_id varchar(10) NOT NULL,
	location_id varchar(10) NOT NULL,
	booking_date date NOT NULL,
	check_in_date date NOT NULL,
	duration int4 NOT NULL,
	total_price numeric(10, 2) NOT NULL,
	CONSTRAINT bookings_duration_check CHECK ((duration >= 0)),
	CONSTRAINT bookings_pkey PRIMARY KEY (booking_id),
	CONSTRAINT bookings_guest_id_fkey FOREIGN KEY (guest_id) REFERENCES bobobox_test_schema.guests(guest_id),
	CONSTRAINT bookings_location_id_fkey FOREIGN KEY (location_id) REFERENCES bobobox_test_schema.locations(location_id)
);