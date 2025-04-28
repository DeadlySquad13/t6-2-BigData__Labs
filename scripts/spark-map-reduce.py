import sys
from pathlib import Path
from pyspark.sql import SparkSession

TOP_N = 10

spark = SparkSession.builder.appName("WordCountRDDExample").getOrCreate()
sc = spark.sparkContext

filename = ""
try:
    filename = sys.argv[1]
except IndexError:
    print("Pass filename as first param")
    exit(1)

data_path = Path("/opt/spark/data/")
file_path = data_path / filename

# Read text file and count words.
df = (
    spark.read.option("delimiter", ",")
    .option("header", True)
    .csv(str(file_path))
)

# Visualize top 10 rows of dataset.
# df.show(10)

word_counts = (
    df.rdd.map(lambda x: x.message)
    .filter(lambda message: message is not None)
    # Remove dots and get all words in a message.
    .flatMap(lambda line: line.replace(".", "").split(" "))
    .map(lambda word: (word, 1))
    .reduceByKey(lambda x, y: x + y)
)

# Sort by count in reverse order (most frequent will be at top).
most_frequent_words = word_counts.sortBy(lambda x: -x[1])

result = most_frequent_words.collect()  # Output: List of (word, count) tuples
for word, count in result[0:TOP_N]:
    print(f"{word}: {count}")
spark.stop()
