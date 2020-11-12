from django.urls import path
from .views import AnswerList, SubmitAnswer, StudentCreate , StudentScore, otpverify ,resendotp


urlpatterns = [
    path('Answer/', AnswerList,name="All Answer"),
    path('sAnswer/<pk>/', SubmitAnswer,name="submit Answer"),
    path('student/', StudentCreate.as_view({'get': 'list', 'post' : 'create'}),name="student signup"),

    # path('student/', StudentCreate.as_view(),name="student signup"),

    path('score/<pk>/', StudentScore,name="Student Score"),

    path('verify/', otpverify,name="Verify otp"),
    path('resendotp/', resendotp,name="resend otp"),

]
