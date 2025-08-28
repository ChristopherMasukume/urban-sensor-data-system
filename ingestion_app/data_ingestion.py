import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import time

def load_environment_variables():
    """Load database credentials from environment variables"""
    load_dotenv()  # Load from .env file if it exists
    return {
        'host': 'postgres-db',
        'database': os.getenv('POSTGRES_DB', 'sensor_data_db'),
        'user': os.getenv('POSTGRES_USER', 'admin_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'secure_password'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }

def create_connection(config, max_retries=5, delay=2):
    """Create database connection with retry logic"""
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**config)
            print("✅ Successfully connected to the database!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"⚠️ Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Waiting {delay} seconds before retry...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise Exception("❌ Could not connect to database after multiple attempts")

def transform_data(df):
    """Transform wide format data to long format, ingesting only numeric columns"""
    print("🔄 Transforming data from wide to long format...")

    # Convert epoch strings to numeric, coerce errors
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    
    # Drop rows with invalid time
    invalid_time_count = df['time'].isna().sum()
    if invalid_time_count > 0:
        print(f"⚠️ Dropping {invalid_time_count} rows with invalid time values...")
        df = df.dropna(subset=['time'])

    # Convert to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)

    # Select only numeric columns for metric_value
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    value_columns = [col for col in numeric_columns if col != 'time']
    print(f"📈 Using {len(value_columns)} numeric columns for ingestion")

    # Melt numeric columns
    transformed_df = df.melt(
        id_vars=['time'],
        value_vars=value_columns,
        var_name='sensor_id',
        value_name='metric_value'
    )
    # Use sensor_id also as metric_name
    transformed_df['metric_name'] = transformed_df['sensor_id']

    print(f"✅ Transformed {len(df)} rows into {len(transformed_df)} measurements")
    print(f"📊 Sample of transformed data:")
    print(transformed_df.head())

    return transformed_df[['time', 'sensor_id', 'metric_name', 'metric_value']]

def ingest_data(conn, df):
    """Ingest transformed data into PostgreSQL"""
    print("📤 Inserting data into database...")
    
    insert_query = """
    INSERT INTO sensor_readings (time, sensor_id, metric_name, metric_value)
    VALUES (%s, %s, %s, %s)
    """
    
    records = []
    for row in df.itertuples(index=False):
        record = tuple(None if pd.isna(x) else x for x in row)
        records.append(record)
    
    batch_size = 10000
    total_records = len(records)
    
    with conn.cursor() as cursor:
        try:
            for i in range(0, total_records, batch_size):
                batch = records[i:i + batch_size]
                cursor.executemany(insert_query, batch)
                conn.commit()
                processed = min(i + batch_size, total_records)
                print(f"✅ Inserted batch {i//batch_size + 1}: {len(batch)} records (total: {processed}/{total_records})")
            
            print(f"🎉 Successfully inserted all {total_records} records!")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error inserting data: {e}")
            raise

def main():
    """Main function to run the data ingestion pipeline"""
    try:
        db_config = load_environment_variables()
        
        print("📖 Reading CSV file...")
        csv_path = r'/app/data/Sensor_Data.csv'

        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
            
        df = pd.read_csv(csv_path, sep=";")
        print(f"✅ Loaded {len(df)} rows from CSV")
        print(f"📊 Dataset columns: {list(df.columns)}")
        print(f"📊 First few rows:")
        print(df.head(2))
        
        transformed_df = transform_data(df)
        conn = create_connection(db_config)
        ingest_data(conn, transformed_df)
        conn.close()
        print("🎉 Data ingestion completed successfully!")
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
