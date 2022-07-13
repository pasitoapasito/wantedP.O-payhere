from django.urls import path

from account_books.views import AccountBookView, AccountBookDetailView, AccountBookRestoreView

urlpatterns = [
    path('', AccountBookView.as_view()),
    path('/<int:account_book_id>', AccountBookDetailView.as_view()),
    path('/<int:account_book_id>/restore', AccountBookRestoreView.as_view()),
]
