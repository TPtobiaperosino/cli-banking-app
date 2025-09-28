# File: /cli-banking-app/cli-banking-app/tests/test_account.py

import unittest
from src.bank.account import BankAccount

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Test Account", 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1200)

    def test_transfer(self):
        target_account = BankAccount("Target Account", 500)
        self.account.transfer(target_account, 200)
        self.assertEqual(self.account.balance, 800)
        self.assertEqual(target_account.balance, 700)

    def test_transfer_insufficient_funds(self):
        target_account = BankAccount("Target Account", 500)
        with self.assertRaises(ValueError):
            self.account.transfer(target_account, 1200)

if __name__ == '__main__':
    unittest.main()