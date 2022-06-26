import datetime

from Domain.Transaction import Transaction


class TransactionValidation:
    @staticmethod
    def validate(transaction: Transaction):
        try:
            date_format = "%d-%m-%Y %H:%M"
            datetime.datetime.strptime(transaction.date_and_hour, date_format)
        except ValueError:
            raise ValueError("Date time format is invalid. ")
