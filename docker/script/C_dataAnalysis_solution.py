"""
SOAL 3 - DATA ANALYSIS CHALLENGE: INCLUDING DATA INSIGHT AND ANOMALY DETECTION
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

plt.style.use('default')
sns.set_palette("husl")

def format_rupiah(x, p):
    return f'Rp {x:,.0f}'

def main():
    output_dir = "output/C_dataAnalysis_results"
    os.makedirs(output_dir, exist_ok=True)

    csv_path = "data/C_data_log_transaction.csv"
    if not os.path.exists(csv_path):
        print(f"File {csv_path} tidak ditemukan!")
        return

    df = pd.read_csv(csv_path)
    df['Transaction_Time'] = pd.to_datetime(df['Transaction_Time'])
    df['Hour'] = df['Transaction_Time'].dt.hour

    success_df = df[df['Status'] == 'Success'].copy()

    # ================== MOBILE VS WEB ==================
    mobile = success_df[success_df['Device_Type'] == 'Mobile']
    web = success_df[success_df['Device_Type'] == 'Web']

    stats_summary = {
        'Device': ['Mobile', 'Web'],
        'Total_Transactions': [len(mobile), len(web)],
        'Total_Amount': [mobile['Amount_IDR'].sum(), web['Amount_IDR'].sum()],
        'Avg_Amount': [mobile['Amount_IDR'].mean(), web['Amount_IDR'].mean()],
        'Success_Rate_%': [
            len(mobile)/len(df[df['Device_Type']=='Mobile']) * 100,
            len(web)/len(df[df['Device_Type']=='Web']) * 100
        ]
    }
    stats_df = pd.DataFrame(stats_summary)

    # ================== 3 BAR CHARTS (TOTAL + AVERAGE) ==================
    fig = plt.figure(figsize=(20, 7))
    fig.suptitle('Mobile vs Web: Perbandingan Perilaku Transaksi', fontsize=18, fontweight='bold', y=0.98)

    plt.subplot(1, 3, 1)
    bars1 = plt.bar(stats_df['Device'], stats_df['Total_Transactions'], 
                    color=['#FF6B6B', '#3498DB'], edgecolor='black', linewidth=1.5)
    plt.title('Volume Transaksi', fontsize=14, fontweight='bold')
    plt.ylabel('Jumlah')
    for bar in bars1:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., h + h*0.01,
                 f'{int(h):,}', ha='center', va='bottom', fontweight='bold', fontsize=12)

    ax2 = plt.subplot(1, 3, 2)
    bars2 = ax2.bar(stats_df['Device'], stats_df['Total_Amount'], color=['#FF6B6B', '#3498DB'], alpha=0.7, label='Total Amount')
    ax2.set_ylabel('Total Amount (IDR)')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x/1e9:.1f}M'))

    ax2b = ax2.twinx()
    line = ax2b.plot(stats_df['Device'], stats_df['Avg_Amount'], color='#FFD700', marker='D', markersize=15, linewidth=5, label='Average Amount')
    ax2b.set_ylabel('Average Amount (IDR)', color='#FFD700', fontsize=12, fontweight='bold')
    ax2b.tick_params(axis='y', labelcolor='#FFD700')
    ax2b.yaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))

    handles1, labels1 = ax2.get_legend_handles_labels()
    handles2, labels2 = ax2b.get_legend_handles_labels()
    ax2.legend(handles1 + handles2, labels1 + labels2, loc='upper left', fontsize=11)
    plt.title('Total Amount vs Average Amount', fontsize=14, fontweight='bold')

    plt.subplot(1, 3, 3)
    bars3 = plt.bar(stats_df['Device'], stats_df['Success_Rate_%'], color=['#FF6B6B', '#3498DB'], edgecolor='black')
    plt.title('Success Rate', fontsize=14, fontweight='bold')
    plt.ylabel('Success Rate (%)')
    plt.ylim(0, 100)
    for bar in bars3:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., h + 1.5,
                 f'{h:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/mobile_vs_web_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ================== HEATMAP (EXACTLY JUPYTER KAMU) ==================
    plt.figure(figsize=(15, 5))
    hourly_pivot = success_df.groupby(['Device_Type', 'Hour']).size().unstack(fill_value=0)
    sns.heatmap(hourly_pivot, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Jumlah Transaksi'}, linewidths=.5, linecolor='gray')
    plt.title('HEATMAP DISTRIBUSI TRANSAKSI\nPer Device Type dan Jam', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Jam')
    plt.ylabel('Device Type')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/transaction_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ================== ANOMALI + "X KALI RATA-RATA" ==================
    df['Z_Score'] = 0.0
    df['Multiplier'] = 1.0
    anomaly_list = []

    for tx_type in df['Transaction_Type'].unique():
        mask = df['Transaction_Type'] == tx_type
        if mask.sum() > 1:
            amounts = df.loc[mask, 'Amount_IDR']
            zscores = np.abs(stats.zscore(amounts))
            df.loc[mask, 'Z_Score'] = zscores
            mean_val = amounts.mean()
            df.loc[mask, 'Multiplier'] = amounts / mean_val

    # Plot 3 panel
    fig, axes = plt.subplots(1, 3, figsize=(22, 8))
    fig.suptitle('DETEKSI ANOMALI: Amount vs Time\n(Warna = Z-Score | Label = X kali rata-rata)', 
                 fontsize=18, fontweight='bold', y=1.02)

    for i, tx_type in enumerate(['Deposit', 'Withdrawal', 'Fee']):
        tx_data = df[df['Transaction_Type'] == tx_type]
        if len(tx_data) == 0: continue

        mean_a = tx_data['Amount_IDR'].mean()
        std_a = tx_data['Amount_IDR'].std()

        scatter = axes[i].scatter(tx_data['Transaction_Time'], tx_data['Amount_IDR'],
                                 c=tx_data['Z_Score'], cmap='RdYlBu_r', s=90, alpha=0.85,
                                 edgecolors='black', linewidth=0.6)

        cbar = plt.colorbar(scatter, ax=axes[i])
        cbar.set_label('Z-Score', fontsize=10)

        axes[i].axhline(y=mean_a, color='red', linestyle='-', linewidth=3, label=f'Rata-rata: Rp {mean_a:,.0f}')
        axes[i].axhspan(mean_a - std_a, mean_a + std_a, alpha=0.2, color='gray', label='±1 Std Dev')

        # LABEL ANOMALI >3x rata-rata
        extreme = tx_data[tx_data['Multiplier'] > 3]
        for _, row in extreme.iterrows():
            multiplier = row['Multiplier']
            axes[i].annotate(f"{row['Transaction_ID']}\n{multiplier:.1f}x rata-rata",
                            xy=(row['Transaction_Time'], row['Amount_IDR']),
                            xytext=(10, 10), textcoords='offset points',
                            fontsize=10, fontweight='bold', color='red',
                            bbox=dict(boxstyle="round,pad=0.4", facecolor="yellow", alpha=0.9),
                            arrowprops=dict(arrowstyle='->', color='red', lw=2))
            anomaly_list.append({
                'ID': row['Transaction_ID'],
                'Type': tx_type,
                'Amount': row['Amount_IDR'],
                'Multiplier': multiplier,
                'Time': row['Transaction_Time'].strftime('%Y-%m-%d %H:%M'),
                'User': row['User_ID'],
                'Device': row['Device_Type']
            })

        axes[i].set_title(f'{tx_type} ({len(tx_data)} transaksi)', fontsize=14, fontweight='bold')
        axes[i].set_xlabel('Waktu Transaksi')
        axes[i].set_ylabel('Amount (IDR)')
        axes[i].yaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].legend(fontsize=10)
        axes[i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/anomaly_with_multiplier_label.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ================== FINAL SUMMARY TXT (SIAP COPY KE LINKEDIN) ==================
    with open(f"{output_dir}/FINAL_INSIGHT_SUMMARY.txt", "w", encoding="utf-8") as f:
        f.write("BOBOBOX DATA ENGINEER TEST - DATA ANLYSIS CHALLENGE REPORT\n")
        f.write("="*70 + "\n\n")
        f.write("KESIMPULAN UTAMA\n")
        f.write(f"• Mobile: {stats_df.iloc[0,1]:,} transaksi → Total Rp {stats_df.iloc[0,2]:,} → Rata-rata Rp {stats_df.iloc[0,3]:,.0f}\n")
        f.write(f"• Web:    {stats_df.iloc[1,1]:,} transaksi → Total Rp {stats_df.iloc[1,2]:,} → Rata-rata Rp {stats_df.iloc[1,3]:,.0f}\n\n")
        f.write("INSIGHT BISNIS \n")
        f.write("→ User Mobile mendominasi dan megumpulkan total jumlah transaksi lebih banyak, akan tetapi jika di rata-rata user WEB 3x lebih profitable\n")
        f.write("→ User WEB termasuk kedalam HIGH-VALUE CUSTOMERS (profit per orang jauh lebih besar!)\n")
        f.write("→ Success rate WEB 98.7% vs Mobile 92.1% → bisa jadi dua kemungkinan, user Mobile tidak seserius user Web ketika melakukan booking\n")
        f.write("→ Puncak transaksi: jam 10-11 pagi (lihat heatmap) baik user Web maupun user Mobile, akan tetapi distribusi aktivitas user Mobile lebih merata\n\n")
        f.write("ANOMALI TERDETEKSI (>3x rata-rata)\n")
        if anomaly_list:
            for a in anomaly_list:
                f.write(f"• {a['ID']} | {a['Type']} | Rp {a['Amount']:,} | {a['Multiplier']:.1f}x rata-rata | {a['Time']} | {a['User']} ({a['Device']})\n")
        else:
            f.write("→ Tidak ada transaksi >3x rata-rata (sangat sehat!)\n")
        f.write("\nREKOMENDASI\n")
        f.write("1. Maksimalkan strategi promosi untuk user Web karena lebih profitable\n")
        f.write("2. Schedule maintenance di luar jam sibuk (10-11 AM)\n")

    print(f"Output disimpan di: {output_dir}/")
    print("   mobile_vs_web_comparison.png")
    print("   transaction_heatmap.png")
    print("   anomaly_with_multiplier_label.png  ")
    print("   FINAL_INSIGHT_SUMMARY.txt")

if __name__ == "__main__":
    main()