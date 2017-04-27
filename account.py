#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#           account class for the bank
#           account.py                  by Paul Short
#                                       paul@jpkweb.com
#                                       using Python v3.6
#  ----------------------------------------------------------------------------------------------------------------------
import pickle

# Primary class to handle all accounts - this is a simple class that can be expanded to include multiple account types
class account():

    nextAcctNumber=0

    # Create a new account instance with an initial balance - if the amount is less than 0, the account will open with
    # a zero balance
    def __init__(self, initialBalance):
        account.nextAcctNumber+=1
        self.accountNumber = account.nextAcctNumber
        if initialBalance < 0:
            self.balance=0
        else:
            self.balance = initialBalance

    # deposit funds into the account
    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            return self.balance
        else:
            return -1

    # Withdraw from account - if there are insufficient funds, it will return -1 and NOT commit the transaction
    def withdraw(self, amount):
        if amount < 0:
            return -1
        if self.balance - amount >= 0:
            self.balance -= amount
            return self.balance
        else:
            return -1

    # Get the balance of the account
    def getBalance(self):
        return self.balance

    def getAccountNumber(self):
        return self.accountNumber

    def saveAccounts(self, name):
        with open(name, 'wb') as handle:
            pickle.dump(self.balance, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadAccounts(self, name):
        with open(name, 'rb') as handle:
            self.balance = pickle.load(handle)

