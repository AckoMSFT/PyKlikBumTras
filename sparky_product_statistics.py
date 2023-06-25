import json

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, lit, coalesce

from sparky_configuration import Configuration

spark = SparkSession.builder.appName('SparkyProductStatistics').getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

product_table_name = 'product'
df_products = spark.read.jdbc(
    Configuration.JDBC_URL,
    product_table_name,
    properties=Configuration.JDBC_PROPERTIES
).withColumnRenamed('id', 'product_id')

order_product_table_name = 'order_product'
df_order_products = spark.read.jdbc(
    Configuration.JDBC_URL,
    order_product_table_name,
    properties=Configuration.JDBC_PROPERTIES
)

order_table_name = 'orders'
df_orders = spark.read.jdbc(
    Configuration.JDBC_URL,
    order_table_name,
    properties=Configuration.JDBC_PROPERTIES
).withColumnRenamed('id', 'order_id')

df_sold = df_products \
    .join(df_order_products, df_products['product_id'] == df_order_products['product_id']) \
    .join(df_orders, df_order_products['order_id'] == df_orders['order_id']) \
    .filter(df_orders['status'] == 'COMPLETE') \
    .groupBy('name').agg(sum('quantity').alias('sold'))

df_waiting = df_products \
    .join(df_order_products, df_products['product_id'] == df_order_products['product_id']) \
    .join(df_orders, df_order_products['order_id'] == df_orders['order_id']) \
    .filter(df_orders['status'] != 'COMPLETE') \
    .groupBy('name').agg(sum('quantity').alias('waiting'))

df_sold = df_sold.withColumnRenamed('name', 'sold_name')
df_waiting = df_waiting.withColumnRenamed('name', 'waiting_name')

df_product_statistics = df_sold \
    .join(df_waiting, df_sold['sold_name'] == df_waiting['waiting_name'], 'full') \
    .select(coalesce(df_sold['sold_name'], df_waiting['waiting_name']).alias('name'),
            coalesce(df_sold['sold'], lit(0)).alias('sold'),
            coalesce(df_waiting['waiting'], lit(0)).alias('waiting')
            )

product_statistics = df_product_statistics.collect()

response = {
    'statistics': [
        {
            'name': product.name,
            'sold': product.sold,
            'waiting': product.waiting,
        } for product in product_statistics
    ]
}
print('SparkyIsABadBadDog!!!!!!!11111111')
print(json.dumps(response))

spark.stop()
