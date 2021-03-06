

from django.urls import path, include, re_path

from .views import ValidatePhoneSendOTP, ValidateOTP, Register

app_name = 'accounts'

urlpatterns = [
    re_path(r'^validate_phone/', ValidatePhoneSendOTP.as_view() ),
    re_path(r'^validate_otp/$', ValidateOTP.as_view() ),
    re_path(r'^register/$', Register.as_view() ),
]
