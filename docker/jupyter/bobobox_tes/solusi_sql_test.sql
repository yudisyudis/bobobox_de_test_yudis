--Write a single SQL query that retrieves the following information for all successful bookings that
--meet these two criteria:
--1. The booking was at a 'Pod' type location AND
--2. The guest provided a rating of 5 in the corresponding review.
--Retrieve the following columns:
--1. Guest_Name
--2. Location_Name
--3. Booking_Date
--4. Previous_Check_Out_Date
--5. Total_Price
--6. Rating
--Previous_Check_Out_Date is the last date the booker ever checks-out before this current
--booking.

with  BookingWithCheckOut as  (
    select  
        *,
        (Check_In_Date + (Duration || ' days')::INTERVAL)::DATE as Check_Out_Date,
        LAG((Check_In_Date + (Duration || ' days')::INTERVAL)::DATE) over  (
            partition by Guest_ID 
            order by Check_In_Date
        ) as Previous_Check_Out_Date
    from Bookings
)
select
    g.Guest_Name,
    l.Location_Name,
    b.Booking_Date,
    b.Total_Price,
    b.Previous_Check_Out_Date,
    r.Rating
from 
    BookingWithCheckOut b 
    join Guests g on g.Guest_ID = b.Guest_ID 
    join Locations l on l.Location_ID = b.Location_ID 
    left join Reviews r on r.Booking_ID = b.Booking_ID 
where 
    l.Type = 'Pod' 
    and r.Rating = 5
;

--Write a single SQL query to calculate the total number of bookings and the average rating for
--each City where Bobobox has locations. Only include cities that have an average rating of 4.0
--or higher and have a total of at least 10 bookings. The results should be ordered by the total
--number of bookings in descending order.

select 
	l.city   , count(b.booking_id) as total_booking , ROUND(AVG(r.rating), 2) as average_rating 
from 
	bookings b 
	join locations l on b.location_id = l.location_id 
	join reviews r on b.booking_id = r.booking_id 
group by l.city
having  
    count(b.Booking_ID) >= 10 
    and avg(r.Rating) >= 4.0
order by total_booking desc;