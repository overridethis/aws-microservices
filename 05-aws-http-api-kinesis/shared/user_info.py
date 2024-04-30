import boto3
import os

USER_POOL_ID = os.environ.get('USER_POOL_ID', None)

class UserInfo:
    def __init__(self):
        self.__client = boto3.client('cognito-idp')

    def get_user_by_id(self, admin_id: str):
        user_info = self.__client.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=admin_id
        )
        return UserInfo.__map(user_info)

    @staticmethod
    def __map(data, attribute_dict_name='UserAttributes'):
        mapped = {
            'id': data['Username'],
            'email': UserInfo.__get_attribute(data, 'email', attribute_dict_name),
            'given_name': UserInfo.__get_attribute(data, 'given_name', attribute_dict_name),
            'family_name': UserInfo.__get_attribute(data, 'family_name', attribute_dict_name),
        }
        return mapped

    @staticmethod
    def __get_attribute(data, attribute_name, attribute_dict_name='UserAttributes'):
        for attribute in data[attribute_dict_name]:
            if attribute['Name'] == attribute_name:
                return attribute['Value']
        return None
