import json
import logging

import utils
from ses_client import SESClient
from services.expenses_service import ExpensesService, ExpensesState
from services.employee_service import EmployeeService, EmployeeRole
import base64

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def __send_notification(email, subject, message):
    body = SESClient.simple_body(subject, message)    
    SESClient().send_email(email, subject, body)

def __get_id_from_record_data(record):
    data = record['kinesis']['data']
    decoded = base64.b64decode(data)
    return json.loads(decoded)['id']

def on_approved(event, context):
    logger.info(f'Event: {event}')
    expense_service = ExpensesService()

    for record in event['Records']:
        expense_id = __get_id_from_record_data(record)
        expense = expense_service.get_by_id(expense_id)

        if not expense:
            logger.error(f'SKIPPED: No expense found. ({expense_id})')
            continue

        if expense.get('status') != ExpensesState.APPROVED.value:
            logger.info(f'SKIPPED: No longer in a approved state. ({expense_id})')
            continue

        requested_by = expense.get('requested_by')
        message = f'Your requested expense for {expense.get("amount")} has been approved.'
        subject = 'Expense Approved (AWS HTTP API Kinesis)'
        __send_notification(requested_by, subject, message)

    return utils.set_response(200, 'Ok')


def on_rejected(event, context):
    logger.info(f'Event: {event}')
    expense_service = ExpensesService()

    for record in event['Records']:
        expense_id = __get_id_from_record_data(record)
        expense = expense_service.get_by_id(expense_id)

        if not expense:
            logger.error(f'SKIPPED: No expense found. ({expense_id})')
            continue

        if expense.get('status') != ExpensesState.REJECTED.value:
            logger.info(f'SKIPPED: No longer in a rejected state. ({expense_id})')
            continue

        requested_by = expense['requested_by']
        message = f'Your requested expense for {expense.get("amount")} has been rejected.'
        subject = 'Expense Rejected (AWS HTTP API Kinesis)'
        __send_notification(requested_by, subject, message)

    return utils.set_response(200, 'Ok')


def on_submitted(event, context):
    logger.info(f'Event: {event}')
    employee_service = EmployeeService()
    expense_service = ExpensesService()

    for record in event['Records']:
        expense_id = __get_id_from_record_data(record)
        expense = expense_service.get_by_id(expense_id)
        if not expense:
            logger.error(f'SKIPPED: No expense found. ({expense_id})')
            continue

        if expense.get('manager'):
            logger.info(f'SKIPPED: Expense already has a manager. ({expense_id})')
            continue

        if expense.get('status') != ExpensesState.SUBMITTED.value:
            logger.info(f'SKIPPED: No longer in a submitted state. ({expense_id})')
            continue

        # Assign manager and notify.
        manager = employee_service.get_by_role(EmployeeRole.MANAGER)[0]
        logger.info(f'Manager: {manager}')
        if not manager:
            logger.error('No manager found.')
            return utils.set_response(400, 'Internal Server Error (No Manager Found)')
        expense_service.assign_manager(expense_id, manager['email'])
        requested_by = expense['requested_by']
        message = f'A expense of {expense.get("amount")} has been requested by {expense.get("requested_by")} and is waiting for your approval.'
        subject = 'Expense Submitted (AWS HTTP API Kinesis)'
        __send_notification(manager['email'], subject, message)

        # Notify employee that expense has been submitted
        requested_by = expense['requested_by']
        message = f'Your requested expense for {expense.get("amount")} has been submitted for approval.'
        __send_notification(requested_by, subject, message)

    return utils.set_response(200, 'Ok')
