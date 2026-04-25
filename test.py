from pyspark.sql import SparkSession

# Build Spark session with cleaner console behavior
spark = (
    SparkSession.builder
    .appName("clean-test")
    .config("spark.ui.showConsoleProgress", "false")  # removes progress bar (fixes shifted text)
    .getOrCreate()
)

# Reduce log verbosity
spark.sparkContext.setLogLevel("ERROR")

# Simple test DataFrame
df = spark.range(5)

# Show result
df.show()

# Stop Spark session
spark.stop()

# cd C:\ETL_JOB
# .\venv\Scripts\Activate.ps1
# python test.py