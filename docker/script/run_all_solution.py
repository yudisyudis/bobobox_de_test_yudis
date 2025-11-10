#!/usr/bin/env python3
"""
Main runner untuk semua solutions
"""

import subprocess
import sys
import time

def run_script(script_name, description):
    """Run Python script dengan error handling"""
    print(f"\n🚀 {description}")
    print("=" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, 
            f"script/{script_name}"
        ], check=True, capture_output=True, text=True)
        
        print(f"✅ {description} completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def wait_for_database():
    """Wait for PostgreSQL database to be ready"""
    print("⏳ Waiting for database to be ready...")
    time.sleep(10)  # Tunggu database startup
    print("✅ Database should be ready now")

def main():
    """Run semua solutions"""
    print("BOTOBOX DATA ENGINEER TEST - ALL SOLUTIONS")
    print("=" * 50)
    
    # Tunggu database ready
    wait_for_database()
    
    # Run Soal 1: Python Challenge
    run_script("A_python_solution.py", "SOAL A: Python Data Challenge")
    
    # Run Soal 2: SQL Query Challenge  
    run_script("B_querySQL_solution.py", "SOAL B: SQL Query Challenge")

    # Run Soal 3: Data Analysis Challenge  
    run_script("C_dataAnalysis_solution.py", "SOAL C: Data Analysis Challenge")
    
    print("\n" + "=" * 50)
    print("ALL SOLUTIONS COMPLETED!")
    print("Check 'output/' folder for results")

if __name__ == "__main__":
    main()