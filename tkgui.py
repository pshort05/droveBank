#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#           I am not a fan of tk for GUI programming, but based on the requirements to only use internal programs
#           tk was the best option, especially since I also went with the latest version of Python for this program
#           If I had a choice I would use wx objects if we needed a true GUI program, or with Django if a web front
#           end would provide the best multiplatform usage
#           tkgui.py                    by Paul Short
#                                       paul@jpkweb.com
#                                       using Python v3.6
#
#           Important Note: I will admit I had to "learn" how to use TK since I have not used it in the past.
#               TK is a built in Python library which should not require additional installation
#  ----------------------------------------------------------------------------------------------------------------------
from dataBase import dataBase
from configSettings import configurationSettings
from account import account

from tkinter import messagebox as msg
import tkinter



# This is the main GUI class using TK
class myGUI(tkinter.Frame):

    # initialize the account classes to be used by the program
    accountList = []
    accountLabels = []

    def __init__(self,parent, *args, **kwargs):
        # Before creating the window we need to handle some variables for this class
        self.isLoggedin=False
        self.isAccountsDisplayed=False

        # This creates the main window with the initial buttons for the bank application
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.lbl0 = tkinter.Label(self, text=" ")
        self.lbl0.grid(column=1, row=1)

        # This will be the main "Status" label for the application
        self.statusLabel = tkinter.Label(self, text="Login to see account data:", relief='sunken' )
        self.statusLabel.grid(column=3, row=2)

        # These will be the account entries that are displayed on the screen
        for i in range(0, 10):
            actLbl = tkinter.Label(self, text=" ")
            actLbl.grid( column=1, row=i+3)
            self.accountLabels.append(actLbl)

        self.btn1 = tkinter.Button(self, width=20, text="Login", command=self.loginEntry)
        self.btn1.grid(column=1, row=0)
        self.btn2 = tkinter.Button(self, width=20, text="Open Account", command=self.createAct)
        self.btn2.grid(column=2, row=0)
        self.btn3 = tkinter.Button(self, width=20, text="Deposit Cash", command=self.depositCashEntry)
        self.btn3.grid(column=3, row=0)
        self.btn4 = tkinter.Button(self, width=20, text="Withdraw Cash", command=self.withdrawCashEntry)
        self.btn4.grid(column=4, row=0)
        self.btn5 = tkinter.Button(self, width=20, text="Transfer Funds", command=self.transferEntry)
        self.btn5.grid(column=5, row=0)
        self.btn6 = tkinter.Button(self, width=20, text="Exit", command=quit)
        self.btn6.grid(column=6, row=0)
        pass

    def displayAccounts(self):
        i=0
        for num in self.accountList:
            tmpName = self.name+str(num.getAccountNumber())
            num.saveAccounts(tmpName)
            tmpTxt= "Account Number: " + str(num.getAccountNumber()) + "   Balance: " + str(num.getBalance())
            self.accountLabels[i].grid_forget()
            self.accountLabels[i] = tkinter.Label(self, text=tmpTxt)
            self.accountLabels[i].grid(column=1, row=i+3)
            i+=1
        pass


    def createAct(self):
        # Create a new account object then add it to the list
        act=account(0)
        self.accountList.append(act)
        self.displayAccounts()

    def transferEntry(self):
        if self.isLoggedin==False:
            self.updateStatus("You must login first!")
            return
        self.tent1 = tkinter.Entry(self, width=10)
        self.tent1.grid(column=5, row=151)
        self.tent2 = tkinter.Entry(self, width=10 )
        self.tent2.grid(column=5, row=152)
        self.tent3 = tkinter.Entry(self, width=10 )
        self.tent3.grid(column=5, row=153)
        self.tbtn7 = tkinter.Button(self, text="Execute", command=self.executeTransfer)
        self.tbtn7.grid(column=5, row=154)
        self.tlbl1 = tkinter.Label(self, text="From Account:")
        self.tlbl1.grid( column=4, row=151)
        self.tlbl2 = tkinter.Label(self, text="To Account:")
        self.tlbl2.grid( column=4, row=152)
        self.tlbl3 = tkinter.Label(self, text="Amount:")
        self.tlbl3.grid( column=4, row=153)
        self.tent1.focus()
        pass

    def executeTransfer(self):
        # get the object for the account FROM
        actFrom = int(self.tent1.get())
        actTo = int(self.tent2.get())
        cash = int(self.tent3.get())
        for num in self.accountList:
            if num.getAccountNumber()==actFrom:
                if num.getBalance()<cash:
                    msg.showerror("Error", "Insufficient Funds!")
                    return
                for num2 in self.accountList:
                    if num2.getAccountNumber()==actTo:
                        num.withdraw(cash)
                        num2.deposit(cash)
                        self.tent1.grid_forget()
                        self.tent2.grid_forget()
                        self.tent3.grid_forget()
                        self.tbtn7.grid_forget()
                        self.tlbl1.grid_forget()
                        self.tlbl2.grid_forget()
                        self.tlbl3.grid_forget()
                        self.displayAccounts()
                        return


        msg.showerror("Error", "Account(s) Not Found")
        self.tent1.grid_forget()
        self.tent2.grid_forget()
        self.tent3.grid_forget()
        self.tbtn7.grid_forget()
        self.tlbl1.grid_forget()
        self.tlbl2.grid_forget()
        self.tlbl3.grid_forget()
        self.displayAccounts()
        return


    def withdrawCashEntry(self):
        if self.isLoggedin==False:
            self.updateStatus("You must login first!")
            return

        self.act = 0
        self.cash1 = 0
        self.went1 = tkinter.Entry(self, width=10)
        self.went1.grid(column=4, row=151)
        self.went2 = tkinter.Entry(self, width=10 )
        self.went2.grid(column=4, row=152)
        self.wbtn7 = tkinter.Button(self, text="Execute", command=self.executeWithdraw)
        self.wbtn7.grid(column=4, row=153)
        self.wlbl1 = tkinter.Label(self, text="Account:")
        self.wlbl1.grid( column=3, row=151)
        self.wlbl2 = tkinter.Label(self, text="Amount:")
        self.wlbl2.grid( column=3, row=152)
        self.went1.focus()
        pass

    def executeWithdraw(self):
        act = int(self.went1.get())
        cash = int(self.went2.get())

        # get the object for the account
        for num in self.accountList:
            if num.getAccountNumber()==act:
                self.went1.grid_forget()
                self.went2.grid_forget()
                self.wbtn7.grid_forget()
                self.wlbl1.grid_forget()
                self.wlbl2.grid_forget()
                result = num.withdraw(cash)
                if result == -1:
                    msg.showerror("Error", "Insufficient Funds!")
                self.displayAccounts()
                return

        msg.showerror("Error", "Account Not Found")
        self.went1.grid_forget()
        self.went2.grid_forget()
        self.wbtn7.grid_forget()
        self.wlbl1.grid_forget()
        self.wlbl2.grid_forget()
        pass

    def depositCashEntry(self):
        if self.isLoggedin==False:
            self.updateStatus("You must login first!")
            return

        # Display Deposit entry items
        self.ent1 = tkinter.Entry(self, width=10)
        self.ent1.grid(column=3, row=151)
        self.ent2 = tkinter.Entry(self, width=10 )
        self.ent2.grid(column=3, row=152)
        self.btn7 = tkinter.Button(self, text="Execute", command=self.executeDeposit)
        self.btn7.grid(column=3, row=153)
        self.slbl1 = tkinter.Label(self, text="Account:")
        self.slbl1.grid( column=2, row=151)
        self.slbl2 = tkinter.Label(self, text="Amount:")
        self.slbl2.grid( column=2, row=152)
        self.ent1.focus()
        pass

    def executeDeposit(self):
        # Get the deposit amounts and verify the account and amounts
        act = int(self.ent1.get())
        cash = int(self.ent2.get())

        # get the object for the account
        for num in self.accountList:
            if num.getAccountNumber()==act:
                self.ent1.grid_forget()
                self.ent2.grid_forget()
                self.btn7.grid_forget()
                self.slbl1.grid_forget()
                self.slbl2.grid_forget()
                num.deposit(cash)
                self.displayAccounts()
                return

        msg.showerror("Error", "Account Not Found")
        self.ent1.grid_forget()
        self.ent2.grid_forget()
        self.btn7.grid_forget()
        self.slbl1.grid_forget()
        self.slbl2.grid_forget()
        pass

    def loginEntry(self):
        self.name=' '
        self.password=' '
        self.lslbl1 = tkinter.Label(self, text="Name:")
        self.lslbl1.grid(column=1, row=151)
        self.lslbl2 = tkinter.Label(self, text="Password:")
        self.lslbl2.grid(column=1, row=152)
        self.lent1 = tkinter.Entry(self, width=10)
        self.lent1.grid(column=2, row=151)
        self.lent2 = tkinter.Entry(self, width=10, show='*')
        self.lent2.grid(column=2, row=152)
        self.lbtn7 = tkinter.Button(self, text="Login", command=self.executeLogin)
        self.lbtn7.grid(column=2, row=153)
        self.lent1.focus()
        pass

    def executeLogin(self):
        accts = configurationSettings(1)

        self.name=self.lent1.get()
        self.password=self.lent2.get()

        # Check if the ID exists - if now ask if you want to create a new one
        if accts.checkID(self.name)==False:
            result = msg.askyesno("Account Not Found", "Do you want to create a new account?")
            if result==True:
                accts.createID(self.name, self.password)
                loginText = "ID " + self.name + " created, login"
                self.updateStatus(loginText)
        else:
            # ID is valid now check if the password matches
            if accts.confirmPassword(self.name, self.password)==False:
                msg.showerror("Error","Incorrect Password")
            else:
                # Update the status label
                self.isLoggedin = True
                loginText = "Logged in as " + self.name
                self.updateStatus(loginText)

        # Load prior accounts


        # Remove the login widgets
        self.lent1.grid_forget()
        self.lent2.grid_forget()
        self.lbtn7.grid_forget()
        self.lslbl1.grid_forget()
        self.lslbl2.grid_forget()
        pass

    def buttonCmd(self,*args,**kwargs):
        pass

    def updateStatus(self, newStatusMsg ):
        self.statusLabel.grid_forget()
        self.statusLabel = tkinter.Label(self, text=newStatusMsg , relief='sunken' )
        self.statusLabel.grid(column=3, row=2)
        pass

# ------------------------- Start the Main Code ------------------------- #
# Define the main window
root = tkinter.Tk()
root.title("Drove Online Piggy Bank - Pigs don't have pockets so they can only own paper bills!")
root.minsize( width=440, height=200 )

MyFrame = myGUI(root)
MyFrame.pack(expand='true',fill='both')

# Start the processing loop
root.mainloop()