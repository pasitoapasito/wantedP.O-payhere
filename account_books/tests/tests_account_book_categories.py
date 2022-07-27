import json

from rest_framework.test  import APITestCase, APIClient

from users.models         import User
from account_books.models import AccountBookCategory


class AccountBookCategoryCreateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(2개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) request body(name/budget)
            - 필수 파라미터 확인
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects\
                       .create_user(
                           email    = 'userTest@example.com',
                           nickname = 'userTest',
                           password = 'Testpassw0rd!'
                       )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.user)
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_create_account_book_category(self):
        data = {
            'name': 'testAccountBookCategory',
        }
        
        response = self.f_client\
                       .post('/api/account-books/categories', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id'      : 1,
                'nickname': 'userTest',
                'name'    : 'testAccountBookCategory',
                'status'  : 'in_use'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_create_account_book_category_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'name': 'testAccountBookCategory',
        }
        
        response = self.client\
                       .post('/api/account-books/categories', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_create_account_book_category_due_to_name_required(self):
        data = {
            'status': 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/categories', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )


class AccountBookCategoryListTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(7개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(1개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) query string(선택 파라미터)
            - search
            - status
            - offset/limit
              * in data range: 데이터 범위내(해당 개수의 데이터 반환)
              * out of data range: 데이터 범위밖(0개의 데이터 반환)
            - sorting
              * up_to_date: 최신순
              * out_of_date: 오래된순
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부 카테고리 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects\
                       .create_user(
                           email    = 'userTest@example.com',
                           nickname = 'userTest',
                           password = 'Testpassw0rd!'
                       )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.user)
        
        AccountBookCategory.objects.create(
            id     = 1,
            users  = cls.user,
            name   = 'testAccountBookCategory1',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 2,
            users  = cls.user,
            name   = 'testAccountBookCategory2',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 3,
            users  = cls.user,
            name   = 'testAccountBookCategory3',
            status = 'deleted'
        )
        
        AccountBookCategory.objects.create(
            id     = 4,
            users  = cls.user,
            name   = 'testAccountBookCategory4',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 5,
            users  = cls.user,
            name   = 'testAccountBookCategory5',
            status = 'deleted'
        )

    """
    성공 케이스 테스트코드
    """
    
    def test_success_list_account_book_category_without_any_condition(self):
        response = self.f_client\
                       .get('/api/account-books/categories', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory4',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory2',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 1,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory1',
                    'status'  : 'in_use'
                }
            ]
        )
        
    def test_success_list_account_book_category_with_search_filter(self):
        search   = '1'
        response = self.f_client\
                       .get(f'/api/account-books/categories?search={search}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 1,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory1',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_category_with_deleted_status_filter(self):
        status   = 'in_use'
        response = self.f_client\
                       .get(f'/api/account-books/categories?status={status}', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 5,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory5',
                    'status'  : 'deleted'
                },
                {
                    'id'      : 3,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory3',
                    'status'  : 'deleted'
                }
            ]
        )
    
    def test_success_list_account_book_category_with_up_to_date_sorting(self):
        sort   = 'up_to_date'
        response = self.f_client\
                       .get(f'/api/account-books/categories?sort={sort}', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory4',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory2',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 1,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory1',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_category_with_out_of_date_sorting(self):
        sort   = 'out_of_date'
        response = self.f_client\
                       .get(f'/api/account-books/categories?sort={sort}', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 1,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory1',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory2',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 4,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory4',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_category_with_offset_limit_in_data_range(self):
        offset   = '0'
        limit    = '2'
        response = self.f_client\
                       .get(f'/api/account-books/categories?offset={offset}&limit={limit}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id'      : 4,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory4',
                    'status'  : 'in_use'
                },
                {
                    'id'      : 2,
                    'nickname': 'userTest',
                    'name'    : 'testAccountBookCategory2',
                    'status'  : 'in_use'
                }
            ]
        )
    
    def test_success_list_account_book_category_with_offset_limit_out_of_data_range(self):
        offset   = '3'
        limit    = '2'
        response = self.f_client\
                       .get(f'/api/account-books/categories?offset={offset}&limit={limit}', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_list_account_book_category_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .get(f'/api/account-books/categories', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    

class AccountBookCategoryUpdateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(3개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) category obj
            - 가계부 카테고리 존재여부 확인(존재하지 않는 카테고리는 수정할 수 없음)
            - 가계부 카테고리 유저정보 확인(다른 유저의 카테고리는 수정할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부 카테고리 정보)
    """

    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
                          )

        self.s_user = User.objects\
                          .create_user(
                              email    = 'testUser@example.com',
                              nickname = 'testUser',
                              password = 'Testpassw3rd!'
                          )
                        
        self.client = APIClient()
        self.client.force_authenticate(user=self.f_user)
        
        AccountBookCategory.objects.create(
            id     = 1,
            users  = self.f_user,
            name   = 'testAccountBookCategory1',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 2,
            users  = self.s_user,
            name   = 'testAccountBookCategory2',
            status = 'in_use'
        )
    
    """
    테스트 데이터 삭제
    """
       
    def tearDown(self):
        User.objects.all().delete()
        AccountBookCategory.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_update_account_book_category(self):
        data = {
            'name'  : 'testAccountBookCategory',
            'status': 'in_use'
        }
        
        response = self.client\
                       .patch('/api/account-books/categories/1', data=json.dumps(data), content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id'      : 1,
                'nickname': 'userTest',
                'name'    : 'testAccountBookCategory',
                'status'  : 'in_use'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
        
    def test_fail_update_account_book_category_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'name'  : 'testAccountBookCategory',
            'status': 'in_use'
        }
        
        response = self.client\
                       .patch('/api/account-books/categories/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_update_account_book_category_due_to_not_existed_category(self):
        data = {
            'name'  : 'testAccountBookCategory',
            'status': 'in_use'
        }
        
        response = self.client\
                       .patch('/api/account-books/categories/10', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_update_account_book_category_due_to_not_own_category(self):
        data = {
            'name'  : 'testAccountBookCategory',
            'status': 'in_use'
        }
        
        response = self.client\
                       .patch('/api/account-books/categories/2', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 카테고리입니다.'
            }
        )


class AccountBookCategoryDeleteTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(4개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) category obj
            - 가계부 카테고리 존재여부 확인(존재하지 않는 카테고리는 삭제할 수 없음)
            - 가계부 카테고리 유저정보 확인(다른 유저의 카테고리는 삭제할 수 없음)
            - 가계부 카테고리 상태정보 확인(이미 삭제된 카테고리는 다시 삭제할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부 카테고리 정보)
    """

    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
                          )

        self.s_user = User.objects\
                          .create_user(
                              email    = 'testUser@example.com',
                              nickname = 'testUser',
                              password = 'Testpassw3rd!'
                          )
                        
        self.client = APIClient()
        self.client.force_authenticate(user=self.f_user)
        
        AccountBookCategory.objects.create(
            id     = 1,
            users  = self.f_user,
            name   = 'testAccountBookCategory1',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 2,
            users  = self.s_user,
            name   = 'testAccountBookCategory2',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 3,
            users  = self.f_user,
            name   = 'testAccountBookCategory3',
            status = 'deleted'
        )
    
    """
    테스트 데이터 삭제
    """   
        
    def tearDown(self):
        User.objects.all().delete()
        AccountBookCategory.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_delete_account_book_category(self):
        response = self.client\
                       .delete('/api/account-books/categories/1', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 1(id)가 삭제되었습니다.'
            }
        )

    """
    실패 케이스 테스트코드
    """
    
    def test_fail_delete_account_book_category_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .delete('/api/account-books/categories/1', content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_delete_account_book_category_due_to_not_existed_category(self):
        response = self.client\
                       .delete('/api/account-books/categories/10', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_delete_account_book_category_due_to_not_own_category(self):
        response = self.client\
                       .delete('/api/account-books/categories/2', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 카테고리입니다.'
            }
        )
        
    def test_fail_delete_account_book_category_due_to_already_deleted_category(self):
        response = self.client\
                       .delete('/api/account-books/categories/3', content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 3(id)는 이미 삭제된 상태입니다.'
            }
        )


class AccountBookCategoryRestoreTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(4개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) category obj
            - 가계부 카테고리 존재여부 확인(존재하지 않는 카테고리는 복구할 수 없음)
            - 가계부 카테고리 유저정보 확인(다른 유저의 카테고리는 복구할 수 없음)
            - 가계부 카테고리 상태정보 확인(이미 복구된 카테고리는 다시 복구할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부 카테고리 정보)
    """
    
    def setUp(self):
        self.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
                          )

        self.s_user = User.objects\
                          .create_user(
                              email    = 'testUser@example.com',
                              nickname = 'testUser',
                              password = 'Testpassw3rd!'
                          )
                        
        self.client = APIClient()
        self.client.force_authenticate(user=self.f_user)
        
        AccountBookCategory.objects.create(
            id     = 1,
            users  = self.f_user,
            name   = 'testAccountBookCategory1',
            status = 'deleted'
        )
        
        AccountBookCategory.objects.create(
            id     = 2,
            users  = self.s_user,
            name   = 'testAccountBookCategory2',
            status = 'deleted'
        )
        
        AccountBookCategory.objects.create(
            id     = 3,
            users  = self.f_user,
            name   = 'testAccountBookCategory3',
            status = 'in_use'
        )
    
    """
    테스트 데이터 삭제
    """
        
    def tearDown(self):
        User.objects.all().delete()
        AccountBookCategory.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_restore_account_book_category(self):
        response = self.client\
                       .patch('/api/account-books/categories/1/restore', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 1(id)가 복구되었습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_restore_account_book_category_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .patch('/api/account-books/categories/1/restore', content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_restore_account_book_category_due_to_not_existed_category(self):
        response = self.client\
                       .patch('/api/account-books/categories/10/restore', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_restore_account_book_category_due_to_not_own_category(self):
        response = self.client\
                       .patch('/api/account-books/categories/2/restore', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 카테고리입니다.'
            }
        )
    
    def test_fail_restore_account_book_category_due_to_already_in_use_category(self):
        response = self.client\
                       .patch('/api/account-books/categories/3/restore', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 3(id)는 이미 사용중입니다.'
            }
        )