

import os
import yaml
from sqlalchemy import create_engine
import logging

log = logging.getLogger(__name__)

# import sys
# import os
# import pandas as pd
# import subprocess
# import argparse
# import pdb
# import pickle


class PostreSQL:
    """
    Copied from datacamp TODO
    """
    def __init__(self):
        self.engine = self.get_database()

        try:
            con = self.engine.raw_connection()
            con.cursor().execute("SET SCHEMA '{}'".format('your_schema_name'))
        except:
            pass

    def get_database(self):
        try:
            engine = self.get_connection_from_profile()
            log.info("Connected to PostgreSQL database!")
        except IOError:
            log.exception("Failed to get database connection!")
            return None, 'fail'

        return engine

    def get_connection_from_profile(self, config_file_name="default_profile.yaml"):
        """
        Sets up database connection from config file.
        Input:
        config_file_name: File containing PGHOST, PGUSER,
                          PGPASSWORD, PGDATABASE, PGPORT, which are the
                          credentials for the PostgreSQL database
        """

        with open(config_file_name, 'r') as f:
            vals = yaml.load(f)

        if not ('PGHOST' in vals.keys() and
                'PGUSER' in vals.keys() and
                'PGPASSWORD' in vals.keys() and
                'PGDATABASE' in vals.keys() and
                'PGPORT' in vals.keys()):
            raise Exception('Bad config file: ' + config_file_name)

        return self.get_engine(vals['PGDATABASE'], vals['PGUSER'],
                          vals['PGHOST'], vals['PGPORT'],
                          vals['PGPASSWORD'])

    def get_engine(self, db, user, host, port, passwd):
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
        engine = create_engine(url, pool_size = 50)
        return engine


