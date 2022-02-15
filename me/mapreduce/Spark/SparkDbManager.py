from me.logger import MeLogger

import pandas as pd
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, TimestampType, FloatType
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp
from datetime import datetime


class SparkDbManager:
    spark_to_pandas = {
        IntegerType().simpleString(): 'int64',
        StringType().simpleString(): 'object',
        BooleanType().simpleString(): 'bool',
        TimestampType().simpleString(): 'datetime64[ns]',
        FloatType().simpleString(): 'float64'
    }

    def __init__(self):
        self.log = MeLogger(name=__name__)
        self.schema = StructType([
            StructField("transaction_id", StringType(), nullable=False),
            StructField("transaction_name", StringType(), nullable=False),
            StructField("account_id", StringType(), nullable=False),
            StructField("account_name", StringType(), nullable=False),
            StructField("amount", IntegerType(), nullable=False),
            StructField("type", StringType(), nullable=True),
            StructField("tx_date", TimestampType(), nullable=False),
            StructField("timestamp", TimestampType(), nullable=False),
            StructField("refunded", BooleanType(), nullable=True),
            StructField("double_checked", BooleanType(), nullable=False),
            StructField("payment", BooleanType(), nullable=False)
        ])

        self.log.debug("Setup Db")
        self.spark = SparkSession.builder \
            .master("local[1]") \
            .appName('AutoAccount') \
            .getOrCreate()

        self.log.debug('Add Test Data')
        # Tests
        example = [(0, 'first transaction null', 0, 'demo', 10, 'demo', datetime.now(), datetime.now(), False, False, True)]
        self.df = self.spark.createDataFrame(data=example, schema=self.schema)
        self.df.printSchema()
        self.df.show(truncate=False)
        #######

    def addTransactions(self, transactions, persist=False, time=datetime.now()):
        """
        Add transactions to database

        :param persist: to persist data on disk
        :arg transactions : Transactions to add to the database (type: pd.DataFrame)
        :arg time : time at which the transactions are added to the db
        """
        transactions['timestamp'] = time
        print(transactions.dtypes)
        new_row = self.spark.createDataFrame(transactions, self.schema)
        self.df = self.df.union(new_row)
        print("New Database :")
        self.df.show(truncate=False)
        print('==============')
        if persist:
            self.df.persist()

    def getTemplate(self):
        return [i.name for i in self.schema], {i.name: SparkDbManager.spark_to_pandas[i.dataType.simpleString()] for i in self.schema}


