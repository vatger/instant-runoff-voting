import json
import os
from urllib import request
from dotenv import load_dotenv


class Limesurvey:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.user_id = -1
        self.url = ''
        self.session_token = ''

        self.__get_credentials()
        self.__get_session_token()

    def __del__(self):
        self.__release_session_token()
        print("Released session token")

    def list_participants(self,
                          survey_id,
                          i_start=0,
                          i_limit=4096,
                          b_unused=None,
                          a_attributes=None,
                          a_conditions=None
                          ) -> list:
        """
        Returns a list containing the specified number of users
        :param survey_id: The survey id from which to query the users from
        :param i_start: The first tid of the user list
        :param i_limit: The last tid of the user list
        :param b_unused:
        :param a_attributes:
        :param a_conditions:
        :return: Returns a list of {tid, token, participant_info: {firstname, lastname, email}}
        """
        print("Running list_participants...")
        params = [
            self.session_token,
            survey_id,
            i_start,
            i_limit,
            b_unused,
            a_attributes,
            a_conditions
        ]
        params = [p for p in params if p is not None]

        res = self.__perform_request({
            'method': 'list_participants',
            'params': params,
            'id': self.user_id
        })

        j_res = json.loads(res)
        d_res = dict(j_res)

        print(f"Got {len(d_res['result'])} participants from survey {survey_id}")
        return d_res['result']

    def add_participants(self, survey_id, users, b_create_token=True):
        res = self.__perform_request({
            'method': 'add_participants',
            'params': [
                self.session_token,
                survey_id,
                users,
                b_create_token
            ],
            'id': self.user_id
        })

        j_res = json.loads(res)
        d_res = dict(j_res)
        return d_res['result']

    def activate_survey(self, survey_id: int):
        res = self.__perform_request({
            'method': 'activate_survey',
            'params': [
                self.session_token,
                survey_id
            ],
            'id': self.user_id
        })

        j_res = json.loads(res)
        d_res = dict(j_res)
        return d_res['result']

    def __get_credentials(self):
        load_dotenv()

        self.username = os.getenv('LS_USERNAME')
        self.user_id = int(os.getenv('LS_UID'))
        self.password = os.getenv('LS_PASSWORD')
        self.url = os.getenv('LS_URL')

        if None in [self.username, self.user_id, self.password, self.url]:
            print(f"Failed to load data from .env. Validate that all entries exist")
            exit(-1)

        print(f"Loaded credentials for {self.username} (UID: {self.user_id})\n"
              f"URL: {self.url}\n"
              f"=========================================================")

    def __perform_request(self, data, method='POST') -> str:
        req = request.Request(self.url, json.dumps(data).encode('utf-8'), method=method)
        req.add_header('content-type', 'application/json')
        req.add_header('connection', 'Keep-Alive')

        res = request.urlopen(req)
        res_data = res.read()
        return res_data

    def __get_session_token(self):
        print("Attempting to retrieve session token...")
        res = self.__perform_request({
            'method': 'get_session_key',
            'params': [
                self.username,
                self.password
            ],
            'id': self.user_id
        })

        j_res = json.loads(res)
        d_res = dict(j_res)

        self.session_token = d_res['result']

    def __release_session_token(self):
        if self.session_token == '':
            return

        self.__perform_request({
            'method': 'release_session_key',
            'params': [
                self.session_token
            ],
            'id': self.user_id
        })
