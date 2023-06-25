import json

from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, sum

from sparky_configuration import Configuration

spark = SparkSession.builder.appName('SparkyCategoryStatistics').getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

product_table_name = 'product'
df_products = spark.read.jdbc(
    Configuration.JDBC_URL,
    product_table_name,
    properties=Configuration.JDBC_PROPERTIES
).withColumnRenamed('id', 'product_id')

category_table_name = 'category'
df_categories = spark.read.jdbc(
    Configuration.JDBC_URL,
    category_table_name,
    properties=Configuration.JDBC_PROPERTIES
).withColumnRenamed('id', 'category_id').withColumnRenamed('name', 'category_name')

product_category_table_name = 'product_category'
df_product_categories = spark.read.jdbc(
    Configuration.JDBC_URL,
    product_category_table_name,
    properties=Configuration.JDBC_PROPERTIES
)

category_statistics = df_product_categories \
    .join(df_products, df_product_categories['product_id'] == df_products['product_id']) \
    .join(df_categories, df_product_categories['category_id'] == df_categories['category_id']) \
    .groupBy('category_name').agg(sum('sold').alias('sum_sold')).sort(desc('sum_sold'), 'category_name').collect()

response = {
    'statistics': [
        category.category_name for category in category_statistics
    ]
}

print('SparkyIsABadBadDog!!!!!!!11111111')
print(json.dumps(response))

spark.stop()
