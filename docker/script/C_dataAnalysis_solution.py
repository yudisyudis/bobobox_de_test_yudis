#!/usr/bin/env python3
"""
Soal 3: Data Insight Analysis
Analisis distribusi transaksi, total amount, dan deteksi anomali dari data_log_transaction.csv
Output: PNG plots + TXT summary di output/soal3_results/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend non-interactive untuk Docker (tanpa display)
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Buat folder output kalau belum ada
    # output_dir = 'output/soal4_results'
    output_dir = os.path.dirname('output/soal4_results')

    os.makedirs(output_dir, exist_ok=True)
    
    # Load data (path relatif dari /app di container)
    data_path = 'data/data_log_transaction.csv'
    if not os.path.exists(data_path):
        print(f"❌ File {data_path} tidak ditemukan! Pastikan ada di ./data/")
        return
    
    df = pd.read_csv(data_path)
    df['Transaction_Time'] = pd.to_datetime(df['Transaction_Time'])
    df['Hour'] = df['Transaction_Time'].dt.hour
    
    print("✅ Data loaded successfully")
    print(f"Shape: {df.shape}")
    
    # 1. Analisis Distribusi per Jam
    hourly_transactions = df.groupby('Hour').size().reset_index(name='Transaction_Count')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Hour', y='Transaction_Count', data=hourly_transactions, palette='viridis')
    plt.title('Transactions per Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Transactions')
    plt.savefig(f'{output_dir}/transactions_per_hour.png', bbox_inches='tight')
    plt.close()
    
    # 2. Analisis per Device
    device_distribution = df.groupby('Device_Type').size().reset_index(name='Count')
    plt.figure(figsize=(8, 8))
    plt.pie(device_distribution['Count'], labels=device_distribution['Device_Type'], autopct='%1.1f%%', startangle=90)
    plt.title('Transaction Distribution by Device Type')
    plt.savefig(f'{output_dir}/transactions_by_device.png', bbox_inches='tight')
    plt.close()
    
    # 3. Analisis per Location
    location_transactions = df.groupby('Location_ID').size().reset_index(name='Transaction_Count')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Location_ID', y='Transaction_Count', data=location_transactions, palette='mako')
    plt.title('Transactions per Location')
    plt.xlabel('Location ID')
    plt.ylabel('Number of Transactions')
    plt.savefig(f'{output_dir}/transactions_per_location.png', bbox_inches='tight')
    plt.close()
    
    # 4. Analisis Total Amount per Type
    total_amount_by_type = df.groupby('Transaction_Type')['Amount_IDR'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Transaction_Type', y='Amount_IDR', data=total_amount_by_type, palette='rocket')
    plt.title('Total Amount by Transaction Type')
    plt.xlabel('Transaction Type')
    plt.ylabel('Total Amount (IDR)')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x:,.0f}'))
    plt.savefig(f'{output_dir}/total_amount_by_type.png', bbox_inches='tight')
    plt.close()
    
    # 5. Deteksi Anomali (Z-Score + IQR)
    df['Z_Score'] = np.nan  # Init kolom Z-Score
    anomaly_summary = []
    
    for tx_type in ['Deposit', 'Withdrawal', 'Fee']:
        tx_data = df[df['Transaction_Type'] == tx_type].copy()
        if len(tx_data) == 0:
            continue
        
        # Z-Score
        mean = tx_data['Amount_IDR'].mean()
        std = tx_data['Amount_IDR'].std()
        tx_data['Z_Score'] = (tx_data['Amount_IDR'] - mean) / std if std != 0 else 0
        df.loc[tx_data.index, 'Z_Score'] = tx_data['Z_Score']
        
        # IQR untuk extreme threshold
        Q1 = tx_data['Amount_IDR'].quantile(0.25)
        Q3 = tx_data['Amount_IDR'].quantile(0.75)
        IQR = Q3 - Q1
        extreme_threshold = Q3 + 3 * IQR
        
        extreme_anomalies = tx_data[tx_data['Amount_IDR'] > extreme_threshold]
        num_anomalies = len(extreme_anomalies)
        
        anomaly_details = f"{tx_type.upper()}:\n"
        anomaly_details += f"  • Q1: Rp {Q1:,.0f}, Q3: Rp {Q3:,.0f}, IQR: Rp {IQR:,.0f}\n"
        anomaly_details += f"  • Extreme threshold (Q3 + 3*IQR): Rp {extreme_threshold:,.0f}\n"
        anomaly_details += f"  • Extreme anomalies ditemukan: {num_anomalies}\n"
        
        if num_anomalies > 0:
            for _, anomaly in extreme_anomalies.iterrows():
                multiplier = anomaly['Amount_IDR'] / mean if mean != 0 else 0
                anomaly_details += f"     🚨 {anomaly['Transaction_ID']}: Rp {anomaly['Amount_IDR']:,.0f} ({multiplier:.1f}x rata-rata)\n"
                anomaly_details += f"        Time: {anomaly['Transaction_Time']}, User: {anomaly['User_ID']}, Device: {anomaly['Device_Type']}\n"
        
        anomaly_summary.append(anomaly_details)
    
    # Simpan summary ke TXT
    with open(f'{output_dir}/anomaly_summary.txt', 'w') as f:
        f.write("INSIGHT SUMMARY:\n")
        f.write(f"- Total Transactions: {len(df)}\n")
        f.write(f"- Peak Hour: {hourly_transactions['Hour'].iloc[hourly_transactions['Transaction_Count'].idxmax()]} ({hourly_transactions['Transaction_Count'].max()} tx)\n")
        f.write(f"- Dominant Device: {device_distribution['Device_Type'].iloc[device_distribution['Count'].idxmax()]} ({device_distribution['Count'].max()} tx)\n")
        f.write(f"- Top Location: {location_transactions['Location_ID'].iloc[location_transactions['Transaction_Count'].idxmax()]} ({location_transactions['Transaction_Count'].max()} tx)\n")
        f.write(f"- Total Amount: Rp {df['Amount_IDR'].sum():,.0f}\n\n")
        f.write("ANOMALY DETECTION:\n")
        f.write("\n".join(anomaly_summary))
    
    print("🎉 All insights generated!")
    print(f"📁 Check '{output_dir}/' for PNG plots and anomaly_summary.txt")

if __name__ == "__main__":
    main()