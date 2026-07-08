import pandas as pd
import click
from tqdm.auto import tqdm
from sqlalchemy import create_engine

chunksize = 100000

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option(
    '--target-table', 
    "target_tables", 
    default=('yellow_taxi_data',), 
    multiple=True, 
    help='Target table name'
)
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_tables):
    for target_table in target_tables:
        df_iter = get_df_iter(target_table)
        engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
        insert_chunks(df_iter, engine, target_table)

def get_df_iter(target_table):
    table_info = {
        "yellow_taxi_data": {
            "url": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz",
            "dtype": {
                "VendorID": "Int64",
                "passenger_count": "Int64",
                "trip_distance": "float64",
                "RatecodeID": "Int64",
                "store_and_fwd_flag": "string",
                "PULocationID": "Int64",
                "DOLocationID": "Int64",
                "payment_type": "Int64",
                "fare_amount": "float64",
                "extra": "float64",
                "mta_tax": "float64",
                "tip_amount": "float64",
                "tolls_amount": "float64",
                "improvement_surcharge": "float64",
                "total_amount": "float64",
                "congestion_surcharge": "float64"
            },
            "parse_dates": [
                "tpep_pickup_datetime",
                "tpep_dropoff_datetime"
            ]
        },
        "zone_lookup": {
            "url": "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
            "dtype": {
                "LocationID": "Int64",
                "Borough": "string",
                "Zone": "string",
                "service_zone": "string"
            }
        }
    }

    if target_table not in table_info:
        raise ValueError(f"Invalid target table: {target_table}. Valid options are: {list(table_info.keys())}")
    
    url = table_info[target_table]["url"]
    dtype = table_info[target_table]["dtype"]
    parse_dates = table_info[target_table].get("parse_dates", None)

    return pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

def insert_chunks(df_iter, engine, target_table):
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=f"{target_table}",
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=f"{target_table}",
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))

if __name__ == "__main__":
    run()