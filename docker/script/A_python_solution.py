import pandas as pd
import re
from datetime import datetime
import os

def load_data():
    # Load data from CSV file
    try:
        data = pd.read_csv('data/A_data_python.csv')
        print(f"Data loaded successfully: {len(data)} rows")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def convert_duration_hours(duration_str):
    # Convert Duration_String to total hours
    if pd.isna(duration_str):
        return 0
    
    duration_str = str(duration_str).lower()
    total_hours = 0
    
    # konversi nilai mengandung days
    days_match = re.search(r'(\d+)\s*day', duration_str)
    if days_match:
        total_hours += int(days_match.group(1)) * 24
    
    # konversi nilai hanya mengandung hours 
    hours_match = re.search(r'(\d+)\s*hour', duration_str)
    if hours_match:
        total_hours += int(hours_match.group(1))
    
    return total_hours

def standardize_guest_type(data):
    # Standardize Guest_Type to New/Returning
    
    # identifikasi variasi guest_type
    variasi = data['Guest_Type'].unique()

    # pengelompokkan kategori guest_type
    var_new = []
    var_returning = []

    for i in variasi:
        guest_type = str(i).lower()
        
        # Cek kategori New
        if any(keyword in guest_type for keyword in ['new', 'baru', 'first']):
            var_new.append(i)
        # Cek kategori Returning  
        elif any(keyword in guest_type for keyword in ['returning', 'repeat', 'kembali']):
            var_returning.append(i)


    # mapping dictionary dari hasil pengelompokkan
    mapping_dict = {}

    # mapping variasi new
    for variant in var_new:
        mapping_dict[variant] = 'New'

    # mapping variasi returning  
    for variant in var_returning:
        mapping_dict[variant] = 'Returning'

    # aplikasikan ke dataframe
    data['Guest_Type'] = data['Guest_Type'].map(mapping_dict)
    
    print("Guest_Type standardization completed")
    return data

def filter_by_date(data):
    # Filter data for Check_In_Date >= 2024-01-01
    
    # ubah tipe data check_in_date menjadi datetime
    data['Check_In_Date'] = pd.to_datetime(data['Check_In_Date'], errors='coerce')
    
    # tentukan batas data terfilter
    limit_date = pd.to_datetime('2024-01-01')
    
    # filter data
    data = data[data['Check_In_Date'] >= limit_date]
    
    print(f"Filtering completed")
    return data

def save_results(data, output_path):
    # Save results to CSV file
    
    # Check if output directory exists, create if not
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        data.to_csv(output_path, index=False)
        
        # Verify file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"Output file created: {output_path} ({file_size} bytes)")
        else:
            print("Output file was not created!")
            
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    """Main function to execute all steps"""
    print("BOTOBOX SOAL A: PYTHON CHALLENGE")
    print("=" * 50)
    
    # Step 1: Load data
    data = load_data()
    if data is None:
        return
    
    print("\n" + "=" * 30)
    
    # Step 2: Convert Duration_String to Stay_Duration_Hours
    data['Stay_Duration_Hours'] = data['Duration_String'].apply(convert_duration_hours)

    
    # Step 3: Standardize Guest_Type
    data = standardize_guest_type(data)
    
    # Step 4: Filter by date
    data = filter_by_date(data)
    
    # Step 5: Display results
    print("FINAL DATA:")
    print(data)
    
    print(f"DATA SUMMARY:")
    print(f"Total records: {len(data)}")
    print(f"New guests: {(data['Guest_Type'] == 'New').sum()}")
    print(f"Returning guests: {(data['Guest_Type'] == 'Returning').sum()}")
    print(f"Date range: {data['Check_In_Date'].min().date()} to {data['Check_In_Date'].max().date()}")
    
    # Step 6: Save results
    output_path = 'output/A_python_result.csv'
    save_results(data, output_path)
    
if __name__ == "__main__":
    main()