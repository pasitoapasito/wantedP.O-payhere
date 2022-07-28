from typing               import Tuple, Any

from account_books.models import AccountBook, AccountBookCategory, AccountBookLog
from users.models         import User

class GetAccountBook:
    """
    Assignee: 김동규
    
    param: account_book_id, user
    return: obj, err
    detail:
      - 가계부 id를 통해 가계부 객체(정보)의 존재여부 확인
      - 가계부 객체의 유저정보와 API를 호출한 유저의 정보를 대조
    """
    
    def get_book_n_check_error(account_book_id: int, user: User) -> Tuple[Any, str]:
        """
        가계부 객체/에러 확인
        """
        try:
            book = AccountBook.objects\
                              .select_related('users')\
                              .get(id=account_book_id)
        except AccountBook.DoesNotExist:
            return None, f'가계부 {account_book_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == book.users.nickname:
            return None, '다른 유저의 가계부입니다.'
        
        return book, None
    

class GetAccountBookCategory:
    """
    Assignee: 김동규
    
    param: account_book_category_id, user
    return: obj, err
    detail:
      - 가계부 카테고리 id를 통해 가계부 카테고리 객체(정보)의 존재여부 확인
      - 가계부 카테고리 객체의 유저정보와 API를 호출한 유저의 정보를 대조
    """
    
    def get_category_n_check_error(account_book_category_id: int, user: User) -> Tuple[Any, str]:
        """
        가계부 카테고리 객체/에러 확인
        """
        try:
            category = AccountBookCategory.objects\
                                          .select_related('users')\
                                          .get(id=account_book_category_id)
        except AccountBookCategory.DoesNotExist:
            return None, f'가계부 카테고리 {account_book_category_id}(id)는 존재하지 않습니다.'
    
        if not user.nickname == category.users.nickname:
            return None, '다른 유저의 가계부 카테고리입니다.'

        return category, None
    

class GetAccountBookLog:
    """
    Assignee: 김동규
    
    param: account_book_log_id, user
    return: obj, err
    detail:
      - 가계부 기록 id를 통해 가계부 기록 객체(정보)의 존재여부 확인
      - 가계부 기록 객체의 유저정보와 API를 호출한 유저의 정보를 대조
    """
    
    def get_log_n_check_error(account_book_log_id: int, book: AccountBook, user: User) -> Tuple[Any, str]:
        """
        가계부 기록 객체/에러 확인
        """
        try:
            log = AccountBookLog.objects\
                                .select_related('books')\
                                .get(id=account_book_log_id)
        except AccountBookLog.DoesNotExist:
            return None, f'가계부 기록 {account_book_log_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == book.users.nickname:
            return None, '다른 유저의 가계부입니다.'
        
        if not user.nickname == log.books.users.nickname:
            return None, '다른 유저의 가계부 기록입니다.'
        
        return log, None