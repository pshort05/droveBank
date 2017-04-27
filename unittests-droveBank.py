#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#           Unit Testing framework using the built-in unittest in Python
#           unittests-droveBank.py      by Paul Short
#                                       paul@jpkweb.com
#                                       using Python v3.6
#  ----------------------------------------------------------------------------------------------------------------------
import unittest
from pathlib import Path
import os


from account import account
class test_account(unittest.TestCase):

    # Basic test to open a new account with a set balance - check for a negitive amount
    def test_getBalance(self):
        myaccount=account(-10)
        myaccount1 = account(10)
        self.assertEqual(myaccount1.getBalance(), 10)
        self.assertNotEqual(myaccount1.getBalance(), 5)
        self.assertEqual(myaccount.getBalance(), 0)

    # Test that funds are withdrawn properly - include check for insufficient funds - check for incorrect funds format (negitive)
    def test_withdrawfunds(self):
        myaccount2 = account(10)
        self.assertEqual( myaccount2.withdraw(5), 5)
        self.assertEqual( myaccount2.withdraw(15), -1)
        self.assertEqual( myaccount2.withdraw(-15), -1)

    # Test adding funds into the account - include check for adding negitive funds
    def test_addfunds(self):
        myaccount3 = account(10)
        self.assertEqual( myaccount3.deposit(10), 20)
        self.assertEqual( myaccount3.deposit(-10), -1)

from configSettings import configurationSettings
class test_configurationSettings(unittest.TestCase):

    # Check to see if an ID is available if not return False, if it is, add it into the system
    def test_checkID(self):
        # I need to remove any prior test configs to fully test!
        tmpFile = 'configuration' + str(11) + '.droveBank'
        File = Path(tmpFile)
        if File.is_file():
            os.remove(tmpFile)

        # Now I can create the new configuration for testing
        myconfig1 = configurationSettings(11)

        # Test to see if an ID exists
        self.assertEqual(myconfig1.checkID('paul'), False)

        # Try to add again and get an error
        myconfig1.createID('paul', 'Password')
        self.assertEqual(myconfig1.checkID('paul'), True)

    # add a new ID then test the password against the new entry
    def test_confirmPassword(self):
        # I need to remove any prior test configs to fully test!
        tmpFile = 'configuration' + str(22) + '.droveBank'
        File = Path(tmpFile)
        if File.is_file():
            os.remove(tmpFile)
        myconfig2 = configurationSettings(22)

        # This will fail since no ID/Password has been created yet
        self.assertEqual(myconfig2.confirmPassword("paul", "Password"), False)

        # add the password into the system
        self.assertEqual(myconfig2.createID("paul", "Password"), True)

        # Now test the password
        self.assertEqual(myconfig2.confirmPassword("paul", "Password"), True)
        self.assertEqual(myconfig2.confirmPassword("paul", "nopass"), False)
        self.assertEqual(myconfig2.confirmPassword("paulk", "Password"), False)


    # return the name of the database from the configuration - to be expanded later
    def test_getDatabaseName(self):
        myconfig3 = configurationSettings(33)
        self.assertEqual( myconfig3.getDatabaseName(), "droveBank.db")


