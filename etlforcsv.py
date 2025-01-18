import pandas as pd
import psycopg2
import os
import random
from datetime import datetime
from holidays import IN as IndianHolidays


# Database credentials
DB_HOST = os.environ.get("DB_HOST", "localhost")  
DB_NAME = os.environ.get("DB_NAME", "Finalproject")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def transform_data(df):
    """Transforms the DataFrame """

    def format_price(price_str):
        if isinstance(price_str, str): #check if its string
            return int(price_str.replace("â‚¹", "").replace(",", "")) if price_str else None #handle empty string
        return price_str

    df['actual_price'] = df['actual_price'].apply(format_price)
    df['discount_price'] = df['discount_price'].apply(format_price)

    in_holidays = IndianHolidays()
    df['festival'] = df['date'].apply(lambda date_str: 1 if datetime.strptime(date_str, '%Y-%m-%d').date() in in_holidays else 0) #date format is assumed to be 'YYYY-MM-DD'

    df['no_of_purchases'] = [random.randint(0, 1000) for _ in range(len(df))]

    df = df[['date', 'name', 'main_category', 'sub_category', 'ratings', 'no_of_ratings', 'festival', 'no_of_purchases', 'actual_price', 'discount_price']]
    df.dropna()

    return df

def save_to_postgres(df, table_name):
    """Saves the DataFrame to a PostgreSQL table."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date DATE,
            name TEXT,
            main_category TEXT,
            sub_category TEXT,
            ratings FLOAT,
            no_of_ratings INTEGER,
            festival INTEGER,
            no_of_purchases INTEGER,
            actual_price INTEGER,
            discount_price INTEGER
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert data to db table
        insert_query = f"""
        INSERT INTO {table_name} (date, name, main_category, sub_category, ratings, no_of_ratings, festival, no_of_purchases, actual_price, discount_price)
        VALUES %s
        """

        from psycopg2.extras import execute_values
        execute_values(cursor, insert_query, df.values.tolist())

        conn.commit()
        print(f"Data successfully saved to {table_name} table.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL or saving data: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def main():
    try:
        
        csv_file_path = "amazondata.csv"  
        df = pd.read_csv(csv_file_path)

        #date in 'YYYY-MM-DD' format.
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        transformed_df = transform_data(df)
        save_to_postgres(transformed_df, "amazontable")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()