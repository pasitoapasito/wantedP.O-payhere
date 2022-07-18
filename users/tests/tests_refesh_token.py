import json

from rest_framework.test             import APITestCase
from rest_framework_simplejwt.tokens import OutstandingToken

from users.models import User


class UserRefreshToken(APITestCase):
    
    maxDiff = None
    
    def setUp(self):
        self.user = User.objects\
                        .create_user(
                            email    = 'userTest@example.com',
                            nickname = 'userTest',
                            password = 'Testpassw0rd!'
                        )
                        
        response = self.client\
                       .post('/api/users/signin',
                             data=json.dumps(
                                 {
                                     'email'   : 'userTest@example.com',
                                     'password': 'Testpassw0rd!'
                                 }
                             ), 
                             content_type='application/json'
                       )                
                        
        self.a_obj = response.json()['access']
        self.r_obj = OutstandingToken.objects\
                                     .get(token=response.json()['refresh'])
                                                  
    def teatDown(self):
        User.objects.all().delete()
        OutstandingToken.objects.all().delete()
    
    def test_success_user_refresh_token(self):
        data = {
            'refresh': self.r_obj.token
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertNotIn('refresh', response.json())
        
    def test_fail_user_refresh_token_due_to_token_required(self):
        data = {
            'refresh': ''
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'refresh': [
                    '이 필드는 blank일 수 없습니다.'
                ]
            }
        )
    
    def test_fail_user_refresh_token_due_to_invalid_token(self):
        data = {
            'refresh': 'fake token'
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '유효하지 않거나 만료된 토큰',
                'code'  : 'token_not_valid'
            }
        )
    
    def test_fail_user_refresh_token_due_to_invalid_token_type(self):
        data = {
            'refresh': self.a_obj
        }
        
        response = self.client\
                       .post('/api/users/token/refresh', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '잘못된 토큰 타입',
                'code'  : 'token_not_valid'
            }
        )