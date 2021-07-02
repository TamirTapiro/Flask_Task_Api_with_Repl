import user.user_manager
import unittest
import requests
import json
import logging
import sys
import random
class TestUserManager(unittest.TestCase):
    my_session = requests.Session()
    base_url = 'http://localhost:5000/api/user'
    
    
    def test_register_exist_user(self):
        res = requests.post(self.base_url + '/register', json={'email': 'tamir@gmail.com', 'password': '1234'})
        self.assertEqual(res.status_code, 409)
    
    def test_login_without_registered_user(self):
        res = requests.post(self.base_url + '/login', json={'email': 'error@gmail.com', 'password': '1234'})
        self.assertEqual(res.status_code, 404)
    
    def test_login_and_login_as_registered_user(self):
        res = self.my_session.post(self.base_url + '/login', json={'email': 'tamir@gmail.com', 'password': '1234'})
        if res.status_code == 200:
            res = self.my_session.post(self.base_url + '/login', json={'email': 'tamir@gmail.com', 'password': '1234'})
            self.assertEqual(res.status_code, 203)
        else:
            self.assertFalse(True)
    
    def test_logout_without_user(self):
        res = requests.post(self.base_url + '/logout', json={'email': 'tamir@gmail.com', 'password': '1234'})
        self.assertEqual(res.status_code, 404)
    
    def test_logout_with_user(self):
        res = self.my_session.post(self.base_url + '/logout')
        self.assertEqual(res.status_code, 200)

class TestTaskManager(unittest.TestCase):
    my_session = requests.Session()
    base_url = 'http://localhost:5000/api/tasks'
    log = logging.getLogger('task_manager')

    def __init__(self, *args, **kwargs):
        super(TestTaskManager, self).__init__(*args, **kwargs)
        self.my_session.post('http://localhost:5000/api/user/login', json={'email': 'tamir@gmail.com', 'password': '1234'})
    
    def test_use_functionality_without_login(self):
        res = requests.get(self.base_url + '/')
        self.assertEqual(res.status_code, 405)
    
    def test_get_all_tasks(self):
        res = self.my_session.get(self.base_url + '/')
        self.assertEqual(res.status_code, 200)
    
    def test_get_all_completed_tasks(self):
        res = self.my_session.get(self.base_url + '/completed')
        if res.status_code == 200:
            res = json.loads(res.content)
            not_completed_list = [item['completed'] for item in res['tasks'] if item['completed'] is False]
            self.assertTrue(len(not_completed_list) == 0)
    
    def test_add_task_with_same_name(self):
        codes = []
        rand_num = random.randint(0,99999999)
        for i in range(2):
            codes.append(self.my_session.post(self.base_url + '/add', json={'name': f'Random Name{rand_num}'}).status_code)
        self.assertEqual(len(codes), 2)
        self.assertEqual(codes[0], 200)
        self.assertEqual(codes[1], 203)
    
    def test_add_task_with_no_name(self):
        self.assertEqual(self.my_session.post(self.base_url + '/add', json={'no_name': ''}).status_code, 403)
