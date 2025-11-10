CREATE TABLE bobobox_test_schema.locations (
	location_id varchar(10) NOT NULL,
	location_name varchar(100) NOT NULL,
	city varchar(50) NOT NULL,
	"type" varchar(10) NULL,
	total_units int4 NOT NULL,
	CONSTRAINT locations_pkey PRIMARY KEY (location_id),
	CONSTRAINT locations_type_check CHECK (((type)::text = ANY ((ARRAY['Pod'::character varying, 'Cabin'::character varying])::text[])))
);
