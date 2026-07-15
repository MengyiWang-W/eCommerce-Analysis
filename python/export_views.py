import sqlite3
import pandas as pd
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

conn = sqlite3.connect('data/processed/ecommerce.db')

views = [
    'agg_orders_daily_revenue',
    'agg_orders_channel_revenue',
    'agg_orders_monthly_revenue',
    'agg_orders_taobao_revenue',
    'agg_orders_shopify_revenue',
    'agg_orders_payment_method_share',
    'agg_orders_daily_channel'
]

export_dir = 'data/processed/exports'
os.makedirs(export_dir, exist_ok=True)

for view in views:
    df = pd.read_sql_query(f"SELECT * FROM {view};", conn)
    csv_path = os.path.join(export_dir, f"{view}.csv")
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"✅ EXPORTED: {view} -> {csv_path} ({len(df)} Rows)")

conn.close()
print("🎉 EXPORTED ALL THE VIEWS SUCCESSFULLY!")

