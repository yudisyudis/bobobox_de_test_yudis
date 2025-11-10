#!/usr/bin/env python3
"""
Soal 2: SQL Query Challenge
CREATED DATABASE, INSERTING SAMPLE DATA, AND DOING SOME WRANGLING DATA WITH SQL
"""

import psycopg2
import pandas as pd
import os
import time

def connect_db():
    """Connect to PostgreSQL dengan retry logic"""
    max_retries = 5
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host="postgres-db",  # Service name di docker-compose
                database="bobobox",
                user="admin",
                password="password",
                port="5432"
            )
            print("Connected to PostgreSQL database")
            return conn
        except Exception as e:
            print(f"❌ Database connection failed (attempt {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(5)
    return None

def execute_query(conn, query, output_file, description):
    """Execute SQL query dan save ke CSV"""
    try:
        df = pd.read_sql_query(query, conn)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        df.to_csv(output_file, index=False)
        # print(f"✅ {description}: {output_file} ({len(df)} rows)")
        
        # # Show sample results
        # print(f"📊 Sample results:")
        # print(df.head(3).to_string(index=False))
        # print()
        
        return df
        
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
        return None

def main():
    """Main function untuk Soal 2"""
    print("BOTOBOX SOAL 2: SQL QUERY CHALLENGE")
    print("=" * 50)
    
    # Connect to database
    conn = connect_db()
    if not conn:
        return
    
    try:
         # QUERY 1: Previous Check Out Date untuk Pod dengan rating 5
        # Write a single SQL query that retrieves the following information for all successful bookings that
        # meet these two criteria:
        # 1. The booking was at a 'Pod' type location AND
        # 2. The guest provided a rating of 5 in the corresponding review.
        # Retrieve the following columns:
        # 1. Guest_Name
        # 2. Location_Name
        # 3. Booking_Date
        # 4. Previous_Check_Out_Date
        # 5. Total_Price
        # 6. Rating

        query1 = """
        with  BookingWithCheckOut as  (
            select  
                *,
                (Check_In_Date + (Duration || ' days')::INTERVAL)::DATE as Check_Out_Date,
                LAG((Check_In_Date + (Duration || ' days')::INTERVAL)::DATE) over  (
                    partition by Guest_ID 
                    order by Check_In_Date
                ) as Previous_Check_Out_Date
            from bobobox_test_schema.bookings
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
            join bobobox_test_schema.guests g ON g.guest_id = b.guest_id 
            join bobobox_test_schema.locations l ON l.location_id = b.location_id 
            left join bobobox_test_schema.reviews r ON r.booking_id = b.booking_id 
        where 
            l.Type = 'Pod' 
            and r.Rating = 5
        ;
        """
        
        execute_query(
            conn, 
            query1, 
            "output/B_query_results/query_1_solutionu.csv",
            "QUERY 1: Booking Pod and 5 sStartar Rated"
        )


        # QUERY 2: Total bookings dan average rating per city
        # Write a single SQL query to calculate the total number of bookings and the average rating for
        # each City where Bobobox has locations. Only include cities that have an average rating of 4.0
        # or higher and have a total of at least 10 bookings. The results should be ordered by the total
        # number of bookings in descending order.

        query2 = """
        select 
            l.city   , count(b.booking_id) as total_booking , ROUND(AVG(r.rating), 2) as average_rating 
        from 
            bobobox_test_schema.bookings b 
            join bobobox_test_schema.locations l on b.location_id = l.location_id 
            join bobobox_test_schema.reviews r on b.booking_id = r.booking_id 
        group by l.city
        having  
            count(b.Booking_ID) >= 10 
            and avg(r.Rating) >= 4.0
        order by total_booking desc;
        """
        
        execute_query(
            conn, 
            query2, 
            "output/B_query_results/query_2_solution.csv",
            "QUERY 2: City booking analysis"
        )
        
       
        print("\n🎉 All SQL queries executed successfully!")
        
    finally:
        conn.close()
        print("🔌 Database connection closed")

if __name__ == "__main__":
    main()