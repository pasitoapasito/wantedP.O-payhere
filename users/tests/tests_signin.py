import json

from rest_framework.test             import APITestCase
from rest_framework_simplejwt.tokens import OutstandingToken

from users.models import User


class UserSignInTest(APITestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        User.objects\
            .create_user(
                email    = 'userTest@example.com',
                nickname = 'userTest',
                password = 'Testpassw0rd!'
            )

    def test_success_user_signin(self):
        data = {
            'email'   : 'userTest@example.com',
            'password': 'Testpassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')
        
        user  = User.objects\
                    .get(email='userTest@example.com')
                    
        token = OutstandingToken.objects\
                                .get(user=user)\
                                .token

        self.assertEqual(response.status_code, 200)
        self.assertEqual(token, response.json()['refresh'])
        
    def test_fail_user_signin_due_to_email_required(self):
        data = {
            'password': 'Testpassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )

    def test_fail_user_signin_due_to_email_mismatch(self):
        data = {
            'email'   : 'testUser@example.com',
            'password': 'Testpassw0rd!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'detail : 올바른 유저정보를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signin_due_to_password_required(self):
        data = {
            'email'   : 'userTest@example.com',
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signin_due_to_password_mismatch(self):
        data = {
            'email'   : 'userTest@example.com',
            'password': 'Testpassword!'
        }
        
        response = self.client\
                       .post('/api/users/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'detail : 올바른 유저정보를 입력하세요.'
                ]
            }
        )