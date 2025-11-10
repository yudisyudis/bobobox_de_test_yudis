CREATE TABLE bobobox_test_schema.guests (
	guest_id varchar(10) NOT NULL,
	guest_name varchar(100) NOT NULL,
	registration_date date NOT NULL,
	CONSTRAINT guests_pkey PRIMARY KEY (guest_id)
);