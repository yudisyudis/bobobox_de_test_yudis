CREATE TABLE bobobox_test_schema.reviews (
	review_id varchar(10) NOT NULL,
	booking_id varchar(10) NOT NULL,
	rating int4 NOT NULL,
	"comment" text NULL,
	review_date date NOT NULL,
	CONSTRAINT reviews_pkey PRIMARY KEY (review_id),
	CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
	CONSTRAINT reviews_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES bobobox_test_schema.bookings(booking_id)
);