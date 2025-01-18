import pandas as pd
import psycopg2
import os

# Database credentials
DB_HOST = os.environ.get("DB_HOST", "localhost")  
DB_NAME = os.environ.get("DB_NAME", "Finalproject")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def extract_from_postgres(table_name, output_csv_path):
    """Extracts data from a PostgreSQL table and saves it to a CSV file."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        
        select_query = f"SELECT * FROM {table_name}"
        cursor.execute(select_query)

        # Fetching all rows from the result set
        rows = cursor.fetchall()

        # Getting column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        
        df = pd.DataFrame(rows, columns=column_names)

        
        df.to_csv(output_csv_path, index=False)  

        print(f"Data successfully extracted from {table_name} and saved to {output_csv_path}")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL or extracting data: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def main():
    try:
        table_name = "amazontable"  
        output_csv_path = "postrgesqldata.csv"  
        extract_from_postgres(table_name, output_csv_path)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()