import json

from datetime             import datetime
from rest_framework.test  import APITestCase, APIClient

from users.models         import User
from account_books.models import AccountBook, AccountBookCategory, AccountBookLog


class AccountBookLogCreateTest(APITestCase):
    '''
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(8개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) query/path param(모두 필수값)
            - book obj: path param
              * 존재하는 가계부인지 확인
              * 본인의 가계부인지 확인
            - category obj: query param
              * 존재하는 카테고리인지 확인
              * 본인의 카테고리인지 확인
        3) request body(title/price)
            - 필수 파라미터 확인
            - 유효한 파라미터인지 확인
    '''
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.f_user = User.objects\
                          .create_user(
                              email    = 'userTest@example.com',
                              nickname = 'userTest',
                              password = 'Testpassw0rd!'
                          )

        cls.s_user = User.objects\
                          .create_user(
                              email    = 'testUser@example.com',
                              nickname = 'testUser',
                              password = 'Testpassw3rd!'
                          )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.f_user)
        
        AccountBook.objects.create(
            id     = 1,
            users  = cls.f_user,
            name   = 'testAccountBook1',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBook.objects.create(
            id     = 2,
            users  = cls.s_user,
            name   = 'testAccountBook2',
            budget = 100000,
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 1,
            users  = cls.f_user,
            name   = 'testAccountBookCategory1',
            status = 'in_use'
        )
        
        AccountBookCategory.objects.create(
            id     = 2,
            users  = cls.s_user,
            name   = 'testAccountBookCategory2',
            status = 'in_use'
        )
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_create_account_book_log(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id'         : 1,
                'title'      : 'testAccountBookLog1',
                'types'      : 'expenditure',
                'price'      : '10000', 
                'description': 'testDescription',
                'status'     : 'in_use',
                'category'   : 'testAccountBookCategory1',
                'book'       : 'testAccountBook1',
                'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
            }
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_create_account_book_log_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.client\
                       .post('/api/account-books/1/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_create_account_book_log_due_to_not_existed_book(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/10/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_own_book(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/2/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_existed_category(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?categories=10', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 카테고리 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_create_account_book_log_due_to_not_own_category(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?categories=2', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 카테고리입니다.'
            }
        )

    def test_fail_create_account_book_log_due_to_title_required(self):
        data = {
            'types'      : 'expenditure',
            'price'      : 10000,
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'title': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_account_book_log_due_to_price_required(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'price': [
                    '이 필드는 필수 항목입니다.'
                ]
            }
        )
    
    def test_fail_create_account_book_log_due_to_invalid_price(self):
        data = {
            'title'      : 'testAccountBookLog1',
            'types'      : 'expenditure',
            'price'      : 'testPrice',
            'description': 'testDescription',
            'status'     : 'in_use'
        }
        
        response = self.f_client\
                       .post('/api/account-books/1/logs?categories=1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'price': [
                    '유효한 숫자를 넣어주세요.'
                ]
            }
        )


class AccountBookLogListTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(12개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(3개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) path param(필수 파라미터)
            - book id
        3) query string(선택 파라미터)
            - search
            - status
            - types
            - categories
            - offset/limit
              * in data range: 데이터 범위내(해당 개수의 데이터 반환)
              * out of data range: 데이터 범위밖(0개의 데이터 반환)
            - sorting
              * up_to_date : 최신순
              * out_of_date: 오래된순
              * high_price : 높은 가격순
              * low_price  : 낮은 가격순
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리/가계부 기록 정보)
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.f_user = User.objects\
                         .create_user(
                             email    = 'userTest@example.com',
                             nickname = 'userTest',
                             password = 'Testpassw0rd!'
                         )
                         
        cls.s_user = User.objects\
                         .create_user(
                             email    = 'testUser@example.com',
                             nickname = 'testUser',
                             password = 'Testpassw3rd!'
                         )
                       
        cls.f_client = APIClient()
        cls.f_client.force_authenticate(user=cls.f_user)
        
        cls.f_book = AccountBook.objects\
                                .create(
                                    id     = 1,
                                    users  = cls.f_user,
                                    name   = 'testAccountBook1',
                                    budget = 100000,
                                    status = 'in_use'
                                )
        
        cls.s_book = AccountBook.objects\
                                .create(
                                    id     = 2,
                                    users  = cls.s_user,
                                    name   = 'testAccountBook2',
                                    budget = 200000,
                                    status = 'in_use'
                                )
        
        cls.f_category = AccountBookCategory.objects\
                                            .create(    
                                                id     = 1,
                                                users  = cls.f_user,
                                                name   = 'testAccountBookCategory1',
                                                status = 'in_use'
                                            )
                                          
        cls.s_category = AccountBookCategory.objects\
                                            .create(
                                                id     = 2,
                                                users  = cls.f_user,
                                                name   = 'testAccountBookCategory2',
                                                status = 'in_use'
                                            )
        
        AccountBookLog.objects.create(
            id          = 1,
            books       = cls.f_book,
            categories  = cls.f_category,
            title       = 'testAccountBookLog1',
            price       = 10000,
            description = 'testDescription1',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 2,
            books       = cls.f_book,
            categories  = cls.f_category,
            title       = 'testAccountBookLog2',
            price       = 20000,
            description = 'testDescription2',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 3,
            books       = cls.f_book,
            categories  = cls.s_category,
            title       = 'testAccountBookLog3',
            price       = 30000,
            description = 'testDescription3',
            types       = 'expenditure',
            status      = 'deleted'
        )
        
        AccountBookLog.objects.create(
            id          = 4,
            books       = cls.f_book,
            categories  = cls.s_category,
            title       = 'testAccountBookLog4',
            price       = 40000,
            description = 'testDescription4',
            types       = 'income',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 5,
            books       = cls.f_book,
            categories  = cls.f_category,
            title       = 'testAccountBookLog5',
            price       = 50000,
            description = 'testDescription5',
            types       = 'income',
            status      = 'deleted'
        )
        
    """
    성공 케이스 테스트코드
    """
        
    def test_success_list_account_book_log_without_any_condition(self):
        response = self.f_client\
                       .get('/api/account-books/1/logs', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )         
    
    def test_success_list_account_book_log_with_search_filter(self):
        search   = 'Log1'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?search={search}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : None,
                'total_expenditure': 10000,
                'logs': [
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
        
    def test_success_list_account_book_log_with_categories_filter(self):
        categories = '1'
        response   = self.f_client\
                         .get(f'/api/account-books/1/logs?categories={categories}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : None,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
        
    def test_success_list_account_book_log_with_deleted_status_filter(self):
        status   = 'in_use'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?status={status}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 50000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 5,
                    'title'      : 'testAccountBookLog5',
                    'types'      : 'income',
                    'price'      : '50000',
                    'description': 'testDescription5',
                    'status'     : 'deleted',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 3,
                    'title'      : 'testAccountBookLog3',
                    'types'      : 'expenditure',
                    'price'      : '30000',
                    'description': 'testDescription3',
                    'status'     : 'deleted',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
        
    def test_success_list_account_book_log_with_up_to_date_sorting(self):
        sort     = 'up_to_date'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_out_of_date_sorting(self):
        sort     = 'out_of_date'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_high_price_sorting(self):
        sort     = 'high_price'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_low_price_sorting(self):
        sort     = 'low_price'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?sort={sort}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_offset_limit_in_data_range(self):
        offset   = '0'
        limit    = '2'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
    
    def test_success_list_account_book_log_with_offset_limit_out_of_data_range(self):
        offset   = '3'
        limit    = '2'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?offset={offset}&limit={limit}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': 30000,
                'logs': []
            }  
        )
    
    def test_success_list_account_book_log_with_income_type(self):
        types    = 'income'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?types={types}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : 40000,
                'total_expenditure': None,
                'logs': [
                    {
                    'id'         : 4,
                    'title'      : 'testAccountBookLog4',
                    'types'      : 'income',
                    'price'      : '40000',
                    'description': 'testDescription4',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory2',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
        
    def test_success_list_account_book_log_with_expenditure_type(self):
        types    = 'expenditure'
        response = self.f_client\
                       .get(f'/api/account-books/1/logs?types={types}', content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'nickname'         : 'userTest',
                'total_income'     : None,
                'total_expenditure': 30000,
                'logs': [
                    {
                    'id'         : 2,
                    'title'      : 'testAccountBookLog2',
                    'types'      : 'expenditure',
                    'price'      : '20000',
                    'description': 'testDescription2',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    },
                    {
                    'id'         : 1,
                    'title'      : 'testAccountBookLog1',
                    'types'      : 'expenditure',
                    'price'      : '10000',
                    'description': 'testDescription1',
                    'status'     : 'in_use',
                    'category'   : 'testAccountBookCategory1',
                    'book'       : 'testAccountBook1',
                    'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                    'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
                    }
                ]
            }  
        )
        
    """
    실패 케이스 테스트코드
    """
            
    def test_fail_list_account_book_log_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .get('/api/account-books/1/logs', content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_list_account_book_log_due_to_not_existed_book(self):
        response = self.f_client\
                       .get('/api/account-books/10/logs', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_list_account_book_log_due_to_not_own_book(self):
        response = self.f_client\
                       .get('/api/account-books/2/logs', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
        

class AccountBookLogUpdateTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(5개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) book obj
            - 가계부 존재여부 확인(존재하지 않는 가계부는 수정할 수 없음)
            - 가계부 유저정보 확인(다른 유저의 가계부는 수정할 수 없음)
        3) log obj
            - 가계부 기록 존재여부 확인(존재하지 않는 기록은 수정할 수 없음)
            - 가계부 기록 유저정보 확인(다른 유저의 기록은 수정할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리/가계부 기록 정보)
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
        
        self.f_book = AccountBook.objects\
                                 .create(
                                     id     = 1,
                                     users  = self.f_user,
                                     name   = 'testAccountBook1',
                                     budget = 100000,
                                     status = 'in_use'
                                 )
        
        self.s_book = AccountBook.objects\
                                 .create(
                                     id     = 2,
                                     users  = self.s_user,
                                     name   = 'testAccountBook2',
                                     budget = 200000,
                                     status = 'in_use'
                                 )
                                 
        self.f_category = AccountBookCategory.objects\
                                             .create(    
                                                 id     = 1,
                                                 users  = self.f_user,
                                                 name   = 'testAccountBookCategory1',
                                                 status = 'in_use'
                                             )
                                          
        self.s_category = AccountBookCategory.objects\
                                             .create(
                                                 id     = 2,
                                                 users  = self.s_user,
                                                 name   = 'testAccountBookCategory2',
                                                 status = 'in_use'
                                             )
        
        AccountBookLog.objects.create(
            id          = 1,
            books       = self.f_book,
            categories  = self.f_category,
            title       = 'testAccountBookLog1',
            price       = 10000,
            description = 'testDescription1',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 2,
            books       = self.s_book,
            categories  = self.s_category,
            title       = 'testAccountBookLog2',
            price       = 20000,
            description = 'testDescription2',
            types       = 'expenditure',
            status      = 'in_use'
        )                                     
    
    """
    테스트 데이터 삭제
    """
        
    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        AccountBookCategory.objects.all().delete()
        AccountBookLog.objects.all().delete()
    
    """
    성공 케이스 테스트코드
    """
        
    def test_success_update_account_book_log(self):
        data = {
            'title'      : 'testAccountBookLog',
            'types'      : 'income',
            'price'      : 100000,
            'description': 'testDescription'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id'         : 1,
                'title'      : 'testAccountBookLog',
                'types'      : 'income',
                'price'      : '100000',
                'description': 'testDescription',
                'status'     : 'in_use',
                'category'   : 'testAccountBookCategory1',
                'book'       : 'testAccountBook1',
                'created_at' : (datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'modified_at': (datetime.now()).strftime('%Y-%m-%d %H:%M')
            }
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_update_account_book_log_due_to_unauthorized_user(self):
        self.client = APIClient()

        data = {
            'title'      : 'testAccountBookLog',
            'types'      : 'income',
            'price'      : 100000,
            'description': 'testDescription'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
        
    def test_fail_update_account_book_log_due_to_not_existed_book(self):
        data = {
            'title'      : 'testAccountBookLog',
            'types'      : 'income',
            'price'      : 100000,
            'description': 'testDescription'
        }

        response = self.client\
                       .patch('/api/account-books/10/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_own_book(self):
        data = {
            'title'      : 'testAccountBookLog',
            'types'      : 'income',
            'price'      : 100000,
            'description': 'testDescription'
        }

        response = self.client\
                       .patch('/api/account-books/2/logs/1', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_existed_log(self):
        data = {
            'title'      : 'testAccountBookLog',
            'types'      : 'income',
            'price'      : 100000,
            'description': 'testDescription'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/10', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 기록 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_update_account_book_log_due_to_not_own_log(self):
        data = {
            'title'      : 'testAccountBookLog',
            'types'      : 'income',
            'price'      : 100000,
            'description': 'testDescription'
        }

        response = self.client\
                       .patch('/api/account-books/1/logs/2', data=json.dumps(data), content_type='application/json')
                       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 기록입니다.'
            }
        )


class AccountBookLogDeleteTest(APITestCase):
    """
    Assignee: 김동규
    
    Test Case Description
    
    1. 케이스 설정 방법
        1) success test case(1개)
            - 테스트 성공 시 성공 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
        2) fail test case(6개) 
            - 테스트 실패 시 에러 응답코드 확인
            - API 응답 데이터가 정상적으로 반환되었는지 확인
    3. Parameters
        1) token(Authentication/Authorization)
            - 인증/인가에 통과한 유저인지 확인(force_authenticate 메소드 사용)
        2) book obj
            - 가계부 존재여부 확인(존재하지 않는 가계부는 삭제할 수 없음)
            - 가계부 유저정보 확인(다른 유저의 가계부는 삭제할 수 없음)
        3) log obj
            - 가계부 기록 존재여부 확인(존재하지 않는 기록은 삭제할 수 없음)
            - 가계부 기록 유저정보 확인(다른 유저의 기록은 삭제할 수 없음)
            - 가계부 기록 상태정보 확인(이미 삭제된 기록은 다시 삭제할 수 없음)
    """
    
    maxDiff = None
    
    """
    테스트 데이터 셋업(유저/가계부/가계부 카테고리/가계부 기록 정보)
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
        
        self.f_book = AccountBook.objects\
                                 .create(
                                     id     = 1,
                                     users  = self.f_user,
                                     name   = 'testAccountBook1',
                                     budget = 100000,
                                     status = 'in_use'
                                 )
        
        self.s_book = AccountBook.objects\
                                 .create(
                                     id     = 2,
                                     users  = self.s_user,
                                     name   = 'testAccountBook2',
                                     budget = 200000,
                                     status = 'in_use'
                                 )
                                 
        self.f_category = AccountBookCategory.objects\
                                             .create(    
                                                 id     = 1,
                                                 users  = self.f_user,
                                                 name   = 'testAccountBookCategory1',
                                                 status = 'in_use'
                                             )
                                          
        self.s_category = AccountBookCategory.objects\
                                             .create(
                                                 id     = 2,
                                                 users  = self.s_user,
                                                 name   = 'testAccountBookCategory2',
                                                 status = 'in_use'
                                             )
        
        AccountBookLog.objects.create(
            id          = 1,
            books       = self.f_book,
            categories  = self.f_category,
            title       = 'testAccountBookLog1',
            price       = 10000,
            description = 'testDescription1',
            types       = 'expenditure',
            status      = 'in_use'
        )
        
        AccountBookLog.objects.create(
            id          = 2,
            books       = self.s_book,
            categories  = self.s_category,
            title       = 'testAccountBookLog2',
            price       = 20000,
            description = 'testDescription2',
            types       = 'expenditure',
            status      = 'in_use'
        )  
        
        AccountBookLog.objects.create(
            id          = 3,
            books       = self.f_book,
            categories  = self.f_category,
            title       = 'testAccountBookLog3',
            price       = 30000,
            description = 'testDescription3',
            types       = 'income',
            status      = 'deleted'
        )                                   
    
    """
    테스트 데이터 삭제
    """
        
    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        AccountBookCategory.objects.all().delete()
        AccountBookLog.objects.all().delete()

    """
    성공 케이스 테스트코드
    """
    
    def test_success_delete_account_book_log(self):
        response = self.client\
                       .delete('/api/account-books/1/logs/1', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 기록 1(id)가 삭제되었습니다.'
            }
        )
    
    """
    실패 케이스 테스트코드
    """
    
    def test_fail_delete_account_book_log_due_to_unauthorized_user(self):
        self.client = APIClient()
        
        response = self.client\
                       .delete('/api/account-books/1/logs/1', content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'
            }
        )
    
    def test_fail_delete_account_book_log_due_to_not_existed_book(self):
        response = self.client\
                       .delete('/api/account-books/10/logs/1', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 10(id)는 존재하지 않습니다.'
            }
        )
        
    def test_fail_delete_account_book_log_due_to_not_own_book(self):
        response = self.client\
                       .delete('/api/account-books/2/logs/1', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부입니다.'
            }
        )
    
    def test_fail_delete_account_book_log_due_to_not_existed_log(self):
        response = self.client\
                       .delete('/api/account-books/1/logs/10', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 기록 10(id)는 존재하지 않습니다.'
            }
        )
    
    def test_fail_delete_account_book_log_due_to_not_own_log(self):
        response = self.client\
                       .delete('/api/account-books/1/logs/2', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '다른 유저의 가계부 기록입니다.'
            }
        )
    
    def test_fail_delete_account_book_log_due_to_already_deleted_log(self):
        response = self.client\
                       .delete('/api/account-books/1/logs/3', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'detail': '가계부 기록 3(id)는 이미 삭제된 상태입니다.'
            }
        )