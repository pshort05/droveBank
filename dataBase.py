#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#           dataBase Class for the DroveBank - this class will use SQLLite for extension into a larger system at
#               a later point in time... For a more extensible system we could use AWS's RDS or a more standard system
#               such as MySQL.  However for RT data requirements memory based database systems provide the best performance
#           dataBase.py                 by Paul Short
#                                       paul@jpkweb.com
#                                       using Python v3.6
#  ----------------------------------------------------------------------------------------------------------------------
import sqlite3
from configSettings import configurationSettings
from pathlib import Path

class dataBase:

    def __init__(self):
        # Get the database name - check if it exists if not, create it
        DBConfig = configurationSettings(1)
        DBFile = DBConfig.getDatabaseName()
        testFile = Path(DBFile)

        # If the file doesn't exist then create the tables
        if testFile.is_file():
            self.db = sqlite3.connect(DBFile)
        else:
            # Once opening the database, the tables must be created
            # - note I used INTEGER's to avoid problems of rounding errors with floating point
            self.db = sqlite3.connect(DBFile)
            self.cursor = db.cursor()
            self.cursor.execute('''
                CREATE TABLE accounts(id INTEGER PRIMARY KEY, name TEXT, balance INTEGER''')
            self.cursor.execute('''
                CREATE TABLE transactions(id INTEGER PRIMARY KEY, datetime TEXT, type TEXT, amount INTEGER''')
            self.cursor.execute('''
                CREATE TABLE nextid(id INTEGER PRIMARY KEY''')
            self.db.commit()



