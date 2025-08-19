from pyspark.sql import SparkSession, functions as F, types as T
import os
import argparse
from .helpers_etl import build_spark

#TODO: Move to classes

def read_input_file(spark: SparkSession, input_path: str, limit: int = None):
    if not (input_path.endswith(".tsv") or input_path.endswith(".tsv.gz")):
        raise NotImplementedError("Not implemented file type")

    reader = (
        spark.read
        .option("sep", "\t")
        .option("header", True)
        .option("multiLine", True)
        .option("quote", '"')
        .option("escape", '"')
    )
    df = reader.csv(input_path)
    if limit:
        df = df.limit(int(limit))

    df = (
        df.select(
            F.col("review_body").alias("text"),
            F.col("star_rating").cast(T.IntegerType()).alias("stars"),
        )
        .where(F.col("text").isNotNull() & F.col("stars").isNotNull())
        .withColumn(
            "label",
            F.when(F.col("stars") >= 4, F.lit("POSITIVE"))
             .when(F.col("stars") <= 2, F.lit("NEGATIVE"))
             .otherwise(F.lit("NEUTRAL")),
        )
    )

    
    return df

def main():
    parser = argparse.ArgumentParser(
        description="ETL Amazon Reviews → Parquet (train/val/test)"
    )
    parser.add_argument(
        "--input", "-i", 
        default = "data/raw/amazon_reviews_us_Electronics_v1_00.tsv.gz",
        help="Input file"
    )
    parser.add_argument(
        "--out",
        "-o",
        default="data/processed",
        help="Output folder",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Used for testing",
    )

    args = parser.parse_args()

    spark = build_spark("amazon-etl")

    df = read_input_file(
        spark,
        input_path=args.input,
        limit=args.limit,
    )

    train, val, test = df.randomSplit([0.7, 0.15, 0.15], seed=42)

    out_path = args.out
    os.makedirs(out_path, exist_ok=True)
    train.write.mode("overwrite").parquet(os.path.join(out_path, "train"))
    val.write.mode("overwrite").parquet(os.path.join(out_path, "val"))
    test.write.mode("overwrite").parquet(os.path.join(out_path, "test"))
    
    #Report
    total = df.count()
    print(f"Total rows: {total}")
    print("Label distribution (train):")
    train.groupBy("label").count().show(truncate=False)

    spark.stop()
    

if __name__=="__main__":
    main()
