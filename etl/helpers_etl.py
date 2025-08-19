from pyspark.sql import SparkSession

DEFAULT_PARTITION = 4
def build_spark(app_name: str, partitions: int = None) -> SparkSession:
    int_partition = partitions or DEFAULT_PARTITION
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.shuffle.partitions", str(int_partition))
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark