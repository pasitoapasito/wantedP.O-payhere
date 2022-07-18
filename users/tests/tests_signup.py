import json

from rest_framework.test import APITestCase

from users.models import User


class UserSignUpTest(APITestCase):
    
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        User.objects\
            .create_user(
                email    = 'userTest@example.com',
                nickname = 'userTest',
                password = 'Testpassw0rd!'
        )
    
    def test_success_user_signup(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'email'   : 'testUser@example.com',
                'nickname': 'testUser'
            }
        )
    
    def test_fail_user_signup_due_to_email_format_validation(self):
        data = {
            'email'   : 'testUserEmail',
            'nickname': 'testUser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '유효한 이메일 주소를 입력하십시오.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_email_required(self):
        data = {
            'nickname': 'testUser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_email(self):
        data = {
            'email'   : 'userTest@example.com',
            'nickname': 'testuser',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    'user의 email은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_email_n_nickname(self):
        data = {
            'email'   : 'userTest@example.com',
            'nickname': 'userTest',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'email': [
                    'user의 email은/는 이미 존재합니다.'
                ],
                'nickname': [
                    'user의 nickname은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_nickname_required(self):
        data = {
            'email'   : 'testUser@example.com',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'nickname': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_already_existed_nickname(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'userTest',
            'password': 'testPassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'nickname': [
                    'user의 nickname은/는 이미 존재합니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_gt_20_digit(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw00000000000000rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_lt_8_digit(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'T3st!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_required(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_small_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'TESTPASSW0RD!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_capital_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testpassw0rd!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_number(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassword!'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_no_special_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw0rd'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )
    
    def test_fail_user_signup_due_to_password_unexpected_special_letters(self):
        data = {
            'email'   : 'testUser@example.com',
            'nickname': 'testUser',
            'password': 'testPassw0rd?'
        }

        response = self.client\
                       .post('/api/users/signup', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'password': [
                    '올바른 비밀번호를 입력하세요.'
                ]
            }
        )