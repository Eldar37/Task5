from decimal import Decimal, InvalidOperation


class BankAccount:
    """Банковский счёт с нулевым начальным балансом."""

    def __init__(self, owner, account_number):
        self.owner = owner
        self.account_number = account_number
        self._balance = Decimal("0")

    @staticmethod
    def _validate_amount(amount):
        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Сумма должна быть числом") from None
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Сумма должна быть положительным конечным числом")
        return amount

    def deposit(self, amount):
        amount = self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        amount = self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount

    def transfer(self, other_account, amount):
        if not isinstance(other_account, BankAccount):
            raise ValueError("Получатель должен быть банковским счётом")
        if other_account is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт")
        amount = self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        other_account._balance += amount

    def get_balance(self):
        return self._balance

    def is_empty(self):
        return self._balance == 0
