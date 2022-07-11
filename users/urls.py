from django.urls import path

from users.views import UserSignUpView, UserSignInView, UserSignOutView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
    path('/signout', UserSignOutView.as_view()),
    path('/token/refresh', TokenRefreshView.as_view()),
]
