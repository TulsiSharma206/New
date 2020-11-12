from django.urls import path
from .views import  login , UserRU, CreateUser, confirmotp, resendotp, resetpassword, passwordchange, logout , ConsultationForm, EnrollForm, BatchList, enrollverify, construcverify, UserPayment, ConfirmPayment, resendcootp, resenderotp, contactUSForm , resendCUotp , contactUSverify , UserPaymentVerify, topicepurchase , topicepurget , userlist, fullcoursep, coursepayment      
from django.contrib.auth import views

urlpatterns = [
    path("login/", login, name="login"),
    path('profile/<int:pk>/', UserRU.as_view(), name='get assignment'),
    path('signup/', CreateUser.as_view(),name="signup"),
    path('confirmaccount/', confirmotp,name="confrim otp"),
    path('resendotp/', resendotp,name="resend otp"),
    path('resetpassword/', resetpassword,name="reset password"),
    path('changepassword/', passwordchange,name="reset password"),
    path("logout/", logout, name="logout"),

    path('consultation/', ConsultationForm.as_view(),name="ConsultationForm"),
    path("enroll/", EnrollForm.as_view(), name="Enroll Form"),

    path('batch/', BatchList.as_view(),name="List Batch"),

    path("everify/", enrollverify, name="enroll verify"),
    path("cverify/", construcverify, name="construction verify"),

    path("coresendotp/", resendcootp, name="consultation resend otp"),

    path("enrollsendotp/", resenderotp, name="enroll resend otp"),

    path("contactus/", contactUSForm.as_view(), name="submit contact form"),
    path("resentcuotp/", resendCUotp, name="contact resend otp"),
    path("contactverify/", contactUSverify, name="Verify contactus"),

    path("upayment/", UserPayment, name="User Direct payment"),
    path("upverify/", UserPaymentVerify, name="user payment Verify"),
    path("cpayment/", ConfirmPayment, name="confirm payment"),

    path("topicepur/", topicepurchase, name="topice purchase"),

    path("topicepurget/<pk>/", topicepurget, name="topice purchase Get"),

    path("userlist/", userlist, name="Alll user list"),

    path("coursepurchase/", fullcoursep, name="Full Course Purchase"),

    path("coursepayment/", coursepayment, name="Course confirm payment"),
]

