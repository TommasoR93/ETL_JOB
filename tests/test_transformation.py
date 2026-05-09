from src.transformation import select_columns, filter_jobs, aggregate_jobs, salary_level
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
import pyspark.sql.functions as F

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[1]")  
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )

    yield spark
    spark.stop()

def test_select_columns(spark):
    data = [
        Row(
            id = 1,
            title = "Data Engineer",
            description = "Build pipelines",
            company=Row(display_name="Acne Corp"),
            salary_min = 5000,
            contract_type = "B2B",
            location=Row(area="Warsaw")
        )
    ]

    input_df = spark.createDataFrame(data)
    print(input_df)
    result_df = select_columns(input_df)

    expected_data = [
        (1, "Data Engineer", "Build pipelines", "Acne Corp", 5000, "B2B", "Warsaw")
    ]

    expected_df = spark.createDataFrame(
        expected_data,
        [
            "job_id",
            "job_title",
            "job_description",
            "company_name",
            "min_salary",
            "contract",
            "location_area"
        ],
    )

    assert result_df.schema == expected_df.schema
    assert sorted(result_df.collect()) == sorted(expected_df.collect())

