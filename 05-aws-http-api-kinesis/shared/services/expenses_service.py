from decimal import Decimal
from enum import Enum

from db_utils import DbUtils
from kinesis_client import KinesisClient
from ses_client import SESClient
import os

TABLE_NAME = 'expenses'
EXPENSE_SUBMITTED_STREAM = os.environ.get('EXPENSE_SUBMITTED_STREAM')
EXPENSE_APPROVED_STREAM = os.environ.get('EXPENSE_APPROVED_STREAM')
EXPENSE_REJECTED_STREAM = os.environ.get('EXPENSE_REJECTED_STREAM')

class ExpensesState(Enum):
    SUBMITTED = 'submitted'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class ExpensesService:
    def __init__(self) -> None:
        self.__db = DbUtils()

    def assign_manager(self, id: str, manager_email: str):
        expense = self.get_by_id(id)
        expense['manager'] = manager_email
        self.__db.put_item(expense, TABLE_NAME)
        return expense

    def mark_as(self, id: str, status: ExpensesState):
        expense = self.get_by_id(id)
        expense['status'] = status.value
        self.__db.put_item(expense, TABLE_NAME)

        if status == ExpensesState.APPROVED:
            KinesisClient.send_record(EXPENSE_APPROVED_STREAM, { 'id': expense.get('id')})
        elif status == ExpensesState.REJECTED:
            KinesisClient.send_record(EXPENSE_REJECTED_STREAM, { 'id': expense.get('id')})

        return expense

    def add_expense(self, 
                    amount: Decimal,
                    date: str,
                    description: str,
                    email: str):
        expense = {
            'amount': Decimal(amount),
            'date': date,
            'description': description,
            'status': ExpensesState.SUBMITTED.value,
            'requested_by': email
        }
        self.__db.put_item(expense, TABLE_NAME)
        KinesisClient.send_record(EXPENSE_SUBMITTED_STREAM, { 'id': expense.get('id') })
        return expense

    def get_by_id(self, id: str):
        return self.__db.get_item({'id': id}, TABLE_NAME)

    def get_all(self):
        return self.__db.scan_for_items(TABLE_NAME)
    
