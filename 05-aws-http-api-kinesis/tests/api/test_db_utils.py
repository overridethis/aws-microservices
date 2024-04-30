from datetime import datetime, timezone

from moto import mock_aws
import tests.layers
import tests.dynamo_db_schema

tests.layers.add_path('api')

import db_utils 

@mock_aws()
class TestDbUtils:

    def __add_expense(self, amount, date, description):
        expense = db_utils.put_item(
            {
                'amount': amount,
                'date': date,
                'description': description
            }
        )
        return expense

    def setup_method(self, method):
        client = db_utils.get_client()
        tests.dynamo_db_schema.add_expenses_table(client)

    def test_put_item(self):
        # arrange.
        expense = self.__add_expense(100, datetime.now(timezone.utc).isoformat(), 'Test')
        # act.
        actual_expense = db_utils.get_item({'id': expense['id']})

        # assert.
        assert actual_expense['amount'] == expense['amount']

    def test_get_items(self):
        # arrange.
        for i in range(10):
            self.__add_expense(100, datetime.now(timezone.utc).isoformat(), f'Test := {i}')

        # act.
        actual_expenses = db_utils.get_items()

        # assert.
        assert len(actual_expenses) >= 10 
