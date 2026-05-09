import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.transformation import transform
from pyspark.sql import SparkSession

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)

# Spark Session
spark = (
    SparkSession.builder
    .appName(os.getenv("SPARK_APP_NAME", "ETL_JOB"))
    .master(os.getenv("SPARK_MASTER", "local[*]"))
    .getOrCreate()
)

# --------------------
# EXTRACT
# --------------------
df = None

for i in range(1, 11):
    temp_df = spark.read.option("multiLine", "true").json(f"data/page_{i}.json")
    df = temp_df if df is None else df.unionByName(temp_df)

# --------------------
# TRANSFORM
# --------------------
df_transf = transform(df)

# --------------------
# LOAD
# --------------------
df_transf.toPandas().to_sql(
    name="jobs",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully.")