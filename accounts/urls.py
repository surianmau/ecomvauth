from django.urls import path , include, re_path
from .views import ValidateUser , Register, LoginAPI

# app_name = "auth"
urlpatterns = [
    re_path(r'^register/',Register.as_view()),
    re_path(r'^login/',LoginAPI.as_view())
    # re_path(r'^validate_otp/', ValidateOTP.as_view()),
]


