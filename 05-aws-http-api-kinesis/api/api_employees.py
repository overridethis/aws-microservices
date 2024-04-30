import logging

import utils
from services.employee_service import EmployeeService, EmployeeRole

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def __is_get_by_id(event):
    route_key = event.get('routeKey')
    return route_key == 'GET /employee/{id}'

def __is_get_by_role(event):
    route_key = event.get('routeKey')
    return route_key == 'GET /employee/byRole/{roleName}'

def handler_get(event):

    service = EmployeeService()

    if __is_get_by_id(event):
        id = event.get('pathParameters').get('id')
        employee = service.get_by_id(id)
        if not employee:
            return utils.set_response(404, 'Not Found (employee)')
        return utils.set_response(200, employee)
    
    if __is_get_by_role(event):
        roleName = event.get('pathParameters').get('roleName')
        employee = service.get_by_role(EmployeeRole[roleName.upper()])
        if not employee:
            return utils.set_response(404, 'Not Found (employee)')
        return utils.set_response(200, employee)
    
    return utils.set_response(200, service.get_all())

def handler_post(event):
    employee = utils.get_body(event)
    if not employee:
        return utils.set_response(400, 'Bad Request (No body)')
    
    service = EmployeeService()
    response = service.add_employee(employee.get('givenName'),
                                    employee.get('familyName'),
                                    employee.get('roleName'),
                                    employee.get('email'))

    return utils.set_response(201, response)

def handler(event, context):
    logger.info(f'Event: {event}')
    method = event.get('requestContext').get('http', {}).get('method')
    logger.info('Method: %s', method)

    if method == 'GET':
        return handler_get(event)
    elif method == 'POST':
        return handler_post(event)
    else:
        return utils.set_response(400, 'Bad Request (Not supported method)')