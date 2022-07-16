from typing               import Tuple, Any

from account_books.models import AccountBook, AccountBookCategory, AccountBookLog
from users.models         import User

class GetAccountBook:
    def get_book_n_check_error(account_book_id: int, user: User) -> Tuple[Any, str]:
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
    def get_category_n_check_error(account_book_category_id: int, user: User) -> Tuple[Any, str]:
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
    def get_log_n_check_error(account_book_log_id: int, user: User) -> Tuple[Any, str]:
        try:
            log = AccountBookLog.objects\
                                .select_related('books')\
                                .get(id=account_book_log_id)
        except AccountBookLog.DoesNotExist:
            return None, f'가계부 기록 {account_book_log_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == log.books.users.nickname:
            return None, '다른 유저의 가계부 기록입니다.'
        
        return log, None