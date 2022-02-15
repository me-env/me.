from me.logger import MeLogger, DEBUG
from me.storage.IDatabase import IDatabase
from me.storage.postgresql.tables import type_to_table, type_to_schema, psql_to_python

import os
import yaml
from sqlalchemy import create_engine


class PostgreSQL(IDatabase):
    def __init__(self):
        self.log = MeLogger(name=__name__, level=DEBUG)
        self.engine = self.connect()
        self.auto_values = ['id', 'timestamp']

        # try: TODO
        self.con = self.engine.raw_connection()
        self.log.debug('con', self.con)
        # self.con.cursor().execute("SET SCHEMA '{}'".format('me_banking'))
        # except:
        #     pass

    def isConnectionValid(self):
        return bool(self.engine) and bool(self.con)

    def connect(self):
        try:
            engine = self.__getConnectionFromProfile()
            self.log.info("Connected to PostgreSQL database!")
        except IOError as e:
            self.log.error("Failed to get database connection!", e)
            return None

        return engine

    def addRow(self, data_type, data):
        """
        Add data 'data' in database (should be one row)
        # TODO make this generic
        # TODO check if the type are correctly formatted to be push
        """
        self.con.cursor().execute("""
            INSERT INTO me_banking.transactions 
            (transaction_id, transaction_name, account_id, account_name, 
            amount, type, tx_date, refunded, double_checked, payment) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (transaction_id, account_id) DO NOTHING;
        """, data)
        self.con.commit()

    def addMultipleRows(self, data_type, data):
        """
        Add data 'data' in database (should be one a list of rows)
        # TODO make this generic
        # TODO check if the type are correctly formatted to be push
        """
        self.log.debug("add multiple rows in psql data:", data)
        data = [list(row.values()) for row in data]
        self.con.cursor().executemany("""
            INSERT INTO me_banking.transactions 
            (transaction_id, transaction_name, account_id, account_name, 
            amount, type, tx_date, refunded, double_checked, payment) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (transaction_id, account_id) DO NOTHING;;
        """, data)
        self.con.commit()

    def reset(self):
        """
        Reset database content
        """
        self.con.cursor().execute("""
            TRUNCATE me_banking.transactions
        """)
        self.con.commit()

    def getScheme(self, data_type, include_auto_fields=False):
        """
        Get Scheme to respect for data type 'data_type'
        :param data_type
        :param include_auto_fields: if True then id fields and timestamp fields are included in scheme
                (please note that these values are supposed to be filled automatically by postgres)
        """
        self.log.debug('datatype value', data_type.value)
        cur = self.con.cursor()
        cur.execute(f"""
            select column_name, data_type from information_schema.columns where 
            table_schema = '{type_to_schema[data_type.value]}' AND 
            table_name = '{type_to_table[data_type.value]}' ORDER BY ordinal_position;
        """)
        res = cur.fetchall()

        check = {i[0]: psql_to_python(i[1], 'check') for i in res if i[0] not in self.auto_values or include_auto_fields}
        convert = {i[0]: psql_to_python(i[1], 'convert') for i in res if i[0] not in self.auto_values or include_auto_fields}
        self.log.debug('return check', check)
        self.log.debug('return convert', convert)
        return check, convert

    def __getConnectionFromProfile(self, config_file_name="default_profile.yaml"):
        """
        Sets up database connection from config file.
        Input:
        config_file_name: File containing PGHOST, PGUSER,
                          PGPASSWORD, PGDATABASE, PGPORT, which are the
                          credentials for the PostgreSQL database
        """

        with open(config_file_name, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        if not ('PGHOST' in config.keys() and
                'PGUSER' in config.keys() and
                'PGPASSWORD' in config.keys() and
                'PGDATABASE' in config.keys() and
                'PGPORT' in config.keys()):
            raise Exception('Bad config file: ' + config_file_name)

        return self.__getEngine(config['PGDATABASE'], config['PGUSER'],
                                config['PGHOST'], config['PGPORT'],
                                config['PGPASSWORD'])

    def __getEngine(self, db, user, host, port, passwd):
        """
        Get SQLalchemy engine using credentials.
        Input:
        db: database name
        user: Username
        host: Hostname of the database server
        port: Port number
        passwd: Password for the database
        """

        url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=user, passwd=passwd, host=host, port=port, db=db)
        self.log.info('Connect to psql with url', url)
        engine = create_engine(url, pool_size=50)
        return engine

    def addTestRow(self):
        self.con.cursor().execute("""
            INSERT INTO me_banking.transactions 
            (transaction_id, transaction_name, account_id, account_name, 
            amount, type, tx_date, timestamp, refunded, double_checked, payment) VALUES 
            ('0001', %s, '00001', 'acc_test', 1.5, '{"type1", "type2"}', '1996-12-02', '1996-12-02', True, False, True);
        """, ('test',))
        self.con.commit()


if __name__ == '__main__':
    db = PostgreSQL()
    db.addTestRow()
