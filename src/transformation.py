import pyspark.sql.functions as F

#Select
def select_columns(df):
        return df.select(
    F.col("id").alias("job_id"),
    F.col("title").alias("job_title"),
    F.col("description").alias("job_description"),
    F.col("company.display_name").alias("company_name"),
    F.col("salary_min").alias("min_salary"),
    F.col("contract_type").alias("contract"),
    F.col("location.area").alias("location_area")
)

#Filtering based on job_title 
def filter_jobs(df):
     return df.filter(
          F.trim(F.col("job_title")).isin(
               "Builder (Self-Employed)",
               "Tiler (Self-Employed)",
               "Painter & Decorator (Self-Employed)"
          )
     )

#Grouping based on job_title, job_description, min_salary, contract, location_area
def aggregate_jobs(df):
     return df.groupBy(
          "job_title",
          "job_description",
          "contract",
          "location_area"          
     ).agg(
          F.sum(F.col("min_salary")).alias("min_salary")
     )
          
#Creating column salary_level conditionally
def salary_level(df):
     return df.withColumn(
         "salary_level",
         F.when(F.col("min_salary") < 30000, "low")
         .when(
              (F.col("min_salary") >= 30000) & (F.col("min_salary") < 50000), "mid"
         )
         .otherwise("high")
     )

def transform(df):
     df = select_columns(df)
     df = filter_jobs(df)
     df = aggregate_jobs(df)
     df = salary_level(df)
     return df



