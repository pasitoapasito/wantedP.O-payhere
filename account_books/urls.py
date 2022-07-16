from django.urls import path

from account_books.views import AccountBookView, AccountBookDetailView, AccountBookRestoreView,\
                                AccountBookCategoryView, AccountBookCategoryDetailView, AccountBookeCategoryRestoreView,\
                                AccountBookLogView, AccountBookLogDetailView

urlpatterns = [
    path('', AccountBookView.as_view()),
    path('/<int:account_book_id>', AccountBookDetailView.as_view()),
    path('/<int:account_book_id>/restore', AccountBookRestoreView.as_view()),
    path('/categories', AccountBookCategoryView.as_view()),
    path('/categories/<int:account_book_category_id>', AccountBookCategoryDetailView.as_view()),
    path('/categories/<int:account_book_category_id>/restore', AccountBookeCategoryRestoreView.as_view()),
    path('/logs/<int:account_book_id>', AccountBookLogView.as_view()),
    path('/logs/<int:account_book_log_id>', AccountBookLogDetailView.as_view()),
]
