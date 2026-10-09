import unittest
from decimal import Decimal

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Эльдар", "001")
        self.receiver = BankAccount("Анна", "002")

    def test_create_account(self):
        self.assertEqual(self.account.owner, "Эльдар")
        self.assertEqual(self.account.account_number, "001")
        self.assertEqual(self.account.get_balance(), 0)
        self.assertTrue(self.account.is_empty())

    def test_deposit(self):
        self.account.deposit(100)
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)
        self.assertFalse(self.account.is_empty())

    def test_fractional_amounts(self):
        self.account.deposit(0.1)
        self.account.deposit(0.2)
        self.assertEqual(self.account.get_balance(), Decimal("0.3"))
        self.account.withdraw(0.3)
        self.assertTrue(self.account.is_empty())

    def test_withdraw(self):
        self.account.deposit(100)
        self.account.withdraw(40)
        self.assertEqual(self.account.get_balance(), 60)

    def test_withdraw_all(self):
        self.account.deposit(100)
        self.account.withdraw(100)
        self.assertEqual(self.account.get_balance(), 0)
        self.assertTrue(self.account.is_empty())

    def test_withdraw_insufficient_funds(self):
        self.account.deposit(100)
        with self.assertRaises(ValueError):
            self.account.withdraw(101)
        self.assertEqual(self.account.get_balance(), 100)

    def test_transfer(self):
        self.account.deposit(100)
        self.receiver.deposit(20)
        self.account.transfer(self.receiver, 40)
        self.assertEqual(self.account.get_balance(), 60)
        self.assertEqual(self.receiver.get_balance(), 60)
        self.assertEqual(
            self.account.get_balance() + self.receiver.get_balance(), 120
        )

    def test_transfer_all(self):
        self.account.deposit(100)
        self.account.transfer(self.receiver, 100)
        self.assertTrue(self.account.is_empty())
        self.assertEqual(self.receiver.get_balance(), 100)

    def test_transfer_insufficient_funds(self):
        self.account.deposit(100)
        self.receiver.deposit(20)
        with self.assertRaises(ValueError):
            self.account.transfer(self.receiver, 101)
        self.assertEqual(self.account.get_balance(), 100)
        self.assertEqual(self.receiver.get_balance(), 20)

    def test_invalid_amounts(self):
        self.account.deposit(100)
        self.receiver.deposit(20)
        operations = (
            self.account.deposit,
            self.account.withdraw,
            lambda amount: self.account.transfer(self.receiver, amount),
        )
        for operation in operations:
            for amount in (-10, 0, "abc", None, True, float("nan"), float("inf")):
                with self.subTest(operation=operation.__name__, amount=amount):
                    with self.assertRaises(ValueError):
                        operation(amount)
                    self.assertEqual(self.account.get_balance(), 100)
                    self.assertEqual(self.receiver.get_balance(), 20)

    def test_invalid_receiver(self):
        self.account.deposit(100)
        with self.assertRaises(ValueError):
            self.account.transfer(None, 10)
        self.assertEqual(self.account.get_balance(), 100)

    def test_transfer_to_self(self):
        self.account.deposit(100)
        with self.assertRaises(ValueError):
            self.account.transfer(self.account, 10)
        self.assertEqual(self.account.get_balance(), 100)

    def test_balance_after_operations(self):
        self.account.deposit(200)
        self.account.withdraw(30)
        self.account.transfer(self.receiver, 50)
        self.assertEqual(self.account.get_balance(), 120)
        self.assertEqual(self.receiver.get_balance(), 50)


if __name__ == "__main__":
    unittest.main()
