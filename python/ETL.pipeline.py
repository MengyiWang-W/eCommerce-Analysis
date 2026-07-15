import pandas as pd 
import sqlite3
import glob
import os

def clean_taobao(df):
    df.rename(columns={'OrderID':'Order_ID','Customer_ID':'Customer_ID','Payment':'Revenue',
                       'Quantity':'Quantity','Category':'Product_Category','Created_At':'Order_Date'},inplace=True)
    df['Order_Date']=pd.to_datetime(df['Order_Date'],format='%Y/%m/%d').dt.strftime('%Y-%m-%d')
    df['Channel']='Taobao'
    return df[['Order_ID','Customer_ID','Revenue','Quantity','Product_Category','Order_Date','Channel']]
def clean_shopify(df):
    df.rename(columns={'OrderID':'Order_ID','Amount':'Amount','Order_Date':'Order_Date','Refund':'Refund','City':'City'},inplace=True)
    df['Order_Date']=pd.to_datetime(df['Order_Date']).dt.strftime('%Y-%m-%d')
    df['Revenue']=df['Amount']-df['Refund'].fillna(0)
    df['Channel']='Shopify'
    return df[['Order_ID','Order_Date','Revenue','Refund','City','Channel']]
def clean_pos(df):
    df.rename(columns={'Transaction_ID':'Order_ID','Payment':'Revenue','Order_Date':'Order_Date','Payment_Method':'Payment_Method'},inplace=True)
    df['Order_Date']=pd.to_datetime(df['Order_Date'],format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
    df['Channel']='POS'
    return df[['Order_ID','Revenue','Order_Date','Payment_Method','Channel']]

def run_ETL():
    all_files=glob.glob("data/raw/*.csv")
    df_all=pd.DataFrame()

    for file in all_files:
        df=pd.read_csv(file)
        if 'taobao' in file:
            df = clean_taobao(df)
        elif 'shopify' in file:
            df = clean_shopify(df)
        elif 'pos' in file:
            df = clean_pos(df)
        else:
            continue
        df_all=pd.concat([df_all,df],ignore_index=True)
    conn=sqlite3.connect('data/processed/ecommerce.db')
    df_all.to_sql('orders',conn,if_exists='replace',index=False)
    conn.close()
    print(f"ETL completed. Total rows: {len(df_all)}")

if __name__=='__main__':
    run_ETL()
