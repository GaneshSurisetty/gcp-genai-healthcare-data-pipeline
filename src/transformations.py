
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, round as spark_round


def main():
    spark = (
        SparkSession.builder
        .appName("HealthcareAnalyticsETL")
        .master("local[*]")
        .getOrCreate()
    )

    input_path = "data/patient_encounters.csv"

    df = spark.read.csv(
        input_path,
        header=True,
        inferSchema=True,
    )

    # Clean and validate healthcare records
    cleaned_df = (
        df.withColumn(
            "claim_amount",
            col("claim_amount").cast("double")
        )
        .filter(col("encounter_id").isNotNull())
        .filter(col("patient_id").isNotNull())
        .filter(col("claim_amount") >= 0)
        .dropDuplicates(["encounter_id"])
    )

    # Aggregate healthcare operational metrics
    analytics_df = (
        cleaned_df.groupBy("encounter_type")
        .agg(
            count("*").alias("total_encounters"),
            spark_round(
                spark_sum("claim_amount"), 2
            ).alias("total_claim_amount"),
        )
    )

    print("\nHealthcare Analytics Summary")
    analytics_df.show(truncate=False)

    output_path = Path("data/output/encounter_analytics")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    analytics_df.coalesce(1).write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path))

    print(f"Analytics output saved to: {output_path}")

    spark.stop()


if __name__ == "__main__":
    main()
