import pandas as pd
from datetime import datetime, timedelta
import random 

# ================= Taobao =================
taobao_orders = []
categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Toys']
for i in range(100000):
    order_id = f"TB{i+1:05d}"
    customer_id = f"C{random.randint(1000, 9999)}"  
    revenue = random.randint(50, 2000)
    quantity = random.randint(1, 5)
    category = random.choice(categories)
    date = (datetime(2024,1,1) + timedelta(days=random.randint(0, 731))).strftime('%Y/%m/%d')
    taobao_orders.append([order_id, customer_id, revenue, quantity, category, date])
df_taobao = pd.DataFrame(taobao_orders, columns=['OrderID', 'Customer_ID', 'Payment', 'Quantity', 'Category', 'Created_At'])
df_taobao.to_csv('data/raw/orders_taobao.csv', index=False, encoding='utf-8-sig')

# ================= Shopify =================
shopify_orders = []
cities = ['New York', 'LA', 'Chicago', 'Houston', 'Miami', 'Seattle']
for i in range(100000):
    order_id = f"SH{i+1:05d}"
    amount = random.randint(30, 2500)
    refund = random.choice([0, 0, 0, random.randint(10, 500)])
    created_at = (datetime(2024,1,1) + timedelta(days=random.randint(0, 731))).isoformat()
    city = random.choice(cities)
    shopify_orders.append([order_id, amount, created_at, refund,city])
df_shopify = pd.DataFrame(shopify_orders, columns=['OrderID','Amount','Order_Date','Refund','City'])
df_shopify.to_csv('data/raw/orders_shopify.csv', index=False)

# ================= Offline POS =================
pos_orders = []
payment_methods = ['WeChat Pay', 'Alipay', 'Credit Card', 'Cash']
for i in range(100000):
    order_id = f"POS{i+1:05d}"
    total = random.randint(20, 3000)
    date = (datetime(2024,1,1) + timedelta(days=random.randint(0, 731))).strftime('%d-%m-%Y')
    payment_method = random.choice(payment_methods)
    pos_orders.append([order_id, total, date,payment_method])
df_pos = pd.DataFrame(pos_orders, columns=['Transaction_ID', 'Payment', 'Order_Date','Payment_Method'])
df_pos.to_csv('data/raw/orders_pos.csv', index=False)

