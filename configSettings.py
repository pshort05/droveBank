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
import pickle
import hashlib
from pathlib import Path

class configurationSettings:

    # Load the configuration settings if they already exist, if not start with a blank set of settings
    def __init__(self, instance):
        """

        :rtype: object
        """
        self.configFile = 'configuration' + str(instance) + '.droveBank'
        confFile = Path(self.configFile)
        if confFile.is_file():
            with open(self.configFile, 'rb') as handle:
                self.IDs = pickle.load(handle)
        else:
            self.IDs = {}

    # Check if a new ID is valid
    # This is where we would insert password requirements for a larger system
    # I am using a simple hash function to store the password - this is not very secure and the ID should be salted before
    # storing the data so it cannot easily be decrypted by brute force (just look at some recent hacks for salted vs unsalted password hashes!)
    # the ID's also must be encrypted and salted as well in production!
    def checkID(self, name ):
        # Check if the ID exists
        if self.IDs.get(name, 0)!=0:
            return True
        else:
            return False

    def createID(self, name, password):
        if self.checkID(name)==True:
            return False
        # The ID is unique, hash the password and store in the dictionary
        hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()
        self.IDs.update({name:hashedPassword})
        with open(self.configFile, 'wb') as handle:
            pickle.dump(self.IDs, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True


    # Check if a current ID/Password is valid
    def confirmPassword(self, name, password):
        hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()
        if self.IDs.get(name)==hashedPassword:
            return True
        else:
            return False

    # Get the database name from the configruation file - initially will be static data
    def getDatabaseName(self):
        return "droveBank.db"



