from rest_framework.filters import SearchFilter
from rest_framework import generics
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from datetime import datetime
from .serializers import UserSerializer , ConsultationSerializer ,EnrollSerializer, BatchSerializer, contactUSSerializer
from rest_framework.views import APIView
from .models import  User, Otp , Consultation , Enroll, Batch, PaymentInfo, contactUS
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import random
import math
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from mcquestions.models import Student, StudentPercentage
from django.http import JsonResponse
from random import randint
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient
from course.models import Course, Purchase, Chapter, FileUpload
import os
import json

import os
from dotenv import load_dotenv
load_dotenv('./.env')
account_sid = os.getenv('TWILLOACCOUT')
auth_token = os.getenv('TWILLOTOKEN')
twilio_phone = os.getenv('TWILLOPHONE')
client = TwilioClient(account_sid, auth_token)
from rest_framework import generics, mixins, permissions
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


@csrf_exempt
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'userid' : user.id, 'username' : user.name},status=HTTP_200_OK)
        else:
            return Response({'status': 'User Account Deactivate'},status=HTTP_400_BAD_REQUEST)
    else:
        try:
            deactive = User.objects.get(email=request.data.get("email"))
            if deactive.is_active == False:
                return Response({'status': 'Please Activate Your Account'},status=HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'status': 'Please Register First'},status=HTTP_401_UNAUTHORIZED)
        
        return Response({'status': 'Your Login Crediations incorrect'},status=HTTP_401_UNAUTHORIZED)
    

def generateOtp(data):
    digits = [i for i in range(0, 10)]
    random_str = str(randint(100000, 999999))
    userid = User.objects.get(contact=data)
    try :
        instance = Otp.objects.get(user=User.objects.get(contact=data))
        instance.delete()
        Otp.objects.create(user_id=int(userid.id),otpu=random_str, created_at=datetime.datetime.now(), expiration_date=timezone.now() + datetime.timedelta(minutes=5))
    except:
        data = Otp.objects.create(user_id=int(userid.id),otpu=random_str, created_at=datetime.datetime.now(), expiration_date=timezone.now() + datetime.timedelta(minutes=5))
    return random_str

@csrf_exempt
@api_view(["POST","GET"])
def confirmotp(request):
    number = request.data.get('mobile_number')

    try:
        userid = User.objects.get(contact=number)
        auth = Otp.objects.get(user_id=userid.id)
        old_date = auth.created_at
        old_date = old_date.replace(tzinfo=None).timestamp()
        current= datetime.datetime.now().timestamp()
        e = current - old_date
        print("e",e)
        if e > 350:
            auth.delete()
            return Response({"status": "Otp Expire"})
        else:
            auth1 = request.data.get('otp')
            if auth.otpu == auth1:
                useractive = User.objects.get(contact=number)
                useractive.is_active =True
                useractive.save()
                auth.delete()
                return Response({"status": "Successfully Create"})
            else:
                return Response({"status": "Wrong Otp"})
    except ObjectDoesNotExist:
        return Response({"status": "Otp Expire"})
    


# Its resend otp and user password reset otp generate both
@csrf_exempt
@api_view(["POST"])
def resendotp(request):
    mobile_number = request.data.get('mobile_number')
    try:
        userid = User.objects.get(contact=mobile_number)
        try:
            re_otp = generateOtp(data=mobile_number)
            client.messages.create(
                body="Please Enter This Otp " + str(re_otp) + " To Register at AspirenowGlobal",
                from_=twilio_phone,
                to=str(mobile_number)
            )
            return JsonResponse(status=200,data={'200':'Otp send successfully'})
        except TwilioRestException:
            return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})
    except ObjectDoesNotExist:
        return JsonResponse(status=403,data={'403':'Mobile Number Not Varified'})


@csrf_exempt
@api_view(["POST"])
def resetpassword(request):
    res_otp = request.data.get('otp')
    number = request.data.get('number')
    try:
        userid = User.objects.get(contact=number)
        auth = Otp.objects.get(user_id=userid.id)
        old_date = auth.created_at
        old_date = old_date.replace(tzinfo=None).timestamp()
        current= datetime.datetime.now().timestamp()
        e = current - old_date
        if e > 350:
            auth.delete()
            return Response({"status": "Otp Expire"})
        else:
            if auth.otpu == res_otp:
                digits = [i for i in range(0, 10)]
                random_str = ""
                for i in range(8):
                    index = math.floor(random.random() * 10)
                    random_str += str(digits[index])
                password = User.objects.get(contact=number)
                password.set_password(random_str)
                password.save()
                user = authenticate(email=password.email, password=random_str)
                if not user:
                    return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,'userId':user.id},status=HTTP_200_OK)
            else:
                return Response({'status': 'Wrong Otp'},status=HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({"status": "Otp Expire"})

# User password change and user forget api and after otp success this api call
@csrf_exempt
@api_view(["POST","GET"])
def passwordchange(request): # Pk Course id
    t = request.META['HTTP_AUTHORIZATION']
    userid=Token.objects.get(key=t)
    password = request.data.get('password')
    c_password = request.data.get('c_password')
    if password != c_password:
        return Response({"Fail": "password Does Not Match"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if userid.user is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            upassword = User.objects.get(email=userid.user)
            upassword.set_password(password)
            upassword.save()
            return Response({"status": "password Change Successfully"})
        
        
class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            inst = serializer.save()
            inst.set_password(inst.password)
            inst.save()
            try:
                mobile_number = request.data['contact']
                re_otp = generateOtp(data=mobile_number)
                client.messages.create(
                    body="Please Enter This Otp " + str(re_otp) + " To Register at AspirenowGlobal",
                    from_=twilio_phone,
                    to=str(mobile_number)
                )
                return JsonResponse(status=202,data={'200':'Otp send successfully'})
            except TwilioRestException:
                return JsonResponse(status=402,data={'402':'Mobile Number Invalid'})

        else:
            return JsonResponse(status=402,data={'402':'Mobile Number Alread Exist'})

    def get_queryset(self):
        return User.objects.all()


    
@csrf_exempt
@api_view(["POST","GET"])
def logout(request): # Pk Course id
    t = request.META['HTTP_AUTHORIZATION']
    try:
        userid=Token.objects.get(key=t)
        userid.delete()
        return Response({"status": "logout Successfully"})
    except Token.DoesNotExist:
        return Response({"status": "already logout"})


class ConsultationForm(generics.CreateAPIView):
    serializer_class = ConsultationSerializer

    def post(self, request, format='json'):
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            inst = serializer.save()
            clientnumber = request.data['number']
            mobile_number = clientnumber
            otp = randint(100000, 999999)
            try:
                client.messages.create(
                    body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
                    from_=twilio_phone,
                    to=str(mobile_number)
                )
                ids = Consultation.objects.filter(number=clientnumber).last()
                conform = Consultation.objects.get(id = ids.id)
                conform.otp = str(otp)
                conform.save()
                return JsonResponse(status=202,data={'200':'Otp send successfully'})
            except TwilioRestException:
                return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})
        else:
            return Resp, Consultation, Enrollonse(serializer.errors, status=400)

    def get_queryset(self):
        return Consultation.objects.all()


@csrf_exempt
@api_view(["POST"])
def resendcootp(request):
    clientnumber = request.data.get('number')
    mobile_number = clientnumber
    otp = randint(100000, 999999)
    try:
        client.messages.create(
            body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
            from_=twilio_phone,
            to=str(mobile_number)
        )
        ids = Consultation.objects.filter(number=clientnumber).last()
        conform = Consultation.objects.get(id = ids.id)
        conform.otp = str(otp)
        conform.save()
        return JsonResponse(status=202,data={'200':'Otp send successfully'})
    except TwilioRestException:
        return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})


@csrf_exempt
@api_view(["POST"])
def resenderotp(request):
    clientnumber = request.data.get('number')
    mobile_number = clientnumber
    otp = randint(100000, 999999)
    try:
        client.messages.create(
            body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
            from_=twilio_phone,
            to=str(mobile_number)
        )
        ids = Enroll.objects.filter(number=clientnumber).last()
        conform = Enroll.objects.get(id = ids.id)
        conform.otp = str(otp)
        conform.save()
        return JsonResponse(status=202,data={'200':'Otp send successfully'})
    except TwilioRestException:
        return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})


class EnrollForm(generics.CreateAPIView):
    serializer_class = EnrollSerializer

    def post(self, request, format='json'):
        serializer = EnrollSerializer(data=request.data)
        if serializer.is_valid():
            inst = serializer.save()
            clientnumber = request.data['number']
            
            mobile_number = clientnumber
            otp = randint(100000, 999999)
            try:
                client.messages.create(
                    body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
                    from_=twilio_phone,
                    to=mobile_number
                )
                ids = Enroll.objects.filter(number=clientnumber).last()
                enform = Enroll.objects.get(id = ids.id)
                enform.otp = str(otp)
                enform.save()
                return JsonResponse(status=202,data={'200':'Otp send successfully'})
            except TwilioRestException:
                return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})
        else:
            return Response(serializer.errors, status=400)

    def get_queryset(self):
        return Enroll.objects.all()


class BatchList(generics.ListAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


@csrf_exempt 
@api_view(["POST"])
def enrollverify(request): 
    mobile_number = request.data['mobile_number']
    otp = int(request.data['otp'])
    try:
        ids = Enroll.objects.filter(number=mobile_number).last()
        ef = Enroll.objects.get(id = ids.id)
    except:
        return JsonResponse(dict(detail="Wrong Mobile Number"))
    otp_timestamp = ef.otpet.replace(tzinfo=None).timestamp()
    current_timestamp = datetime.datetime.now().timestamp()
    e = current_timestamp - otp_timestamp
    print("e",e)
    if e < 350:
        if otp == int(ef.otp):
            ef.is_verify = True
            ef.save()

            subject = 'Inquiry Request'
            message = f"Hi Admin \none candidate has Enroll Now  \n user : {ef.name}, \n email : {ef.email},\n number : {ef.number}, \n course : {ef.course} "
            
            clientemail = 'info@aspirenowglobal.com'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [clientemail,]
            send_mail( subject, message, email_from, recipient_list)

            return JsonResponse(dict(detail="Verify Successfully "),status=200,)
        else:
            return JsonResponse(dict(detail="The provided code did not match "),status=401,)
    else:
        return JsonResponse(dict(detail="The provided code has expired"),status=401,)


@csrf_exempt 
@api_view(["POST"])
def construcverify(request): 
    mobile_number = request.data['mobile_number']
    otp = int(request.data['otp'])
    try:
        ids = Consultation.objects.filter(number=mobile_number).last()
        ef = Consultation.objects.get(id = ids.id)
    except:
        return JsonResponse(dict(detail="Wrong Mobile Number"))
    otp_timestamp = ef.otpct.replace(tzinfo=None).timestamp()
    current_timestamp = datetime.datetime.now().timestamp()
    e = current_timestamp - otp_timestamp
    print("e",e)
    if e < 350:
        if otp == int(ef.otp):
            ef.is_verify = True
            ef.save()

            subject = 'Inquiry Request'
            message = f"Hi Admin \none candidate has counseling  \n user : {ef.name}, \n email : {ef.email},\n number : {ef.number}, \n course : {ef.course}, \n day : {ef.day}, \n time : {ef.time} "
            
            clientemail = 'info@aspirenowglobal.com'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [clientemail,]

            send_mail( subject, message, email_from, recipient_list)

            return JsonResponse(dict(detail="Verify Successfully "),status=200,)
        else:
            return JsonResponse(dict(detail="The provided code did not match "),status=401,)
    else:
        return JsonResponse(dict(detail="The provided code has expired"),status=401,)
 

class contactUSForm(generics.CreateAPIView):
    serializer_class = contactUSSerializer

    def post(self, request, format='json'):
        serializer = contactUSSerializer(data=request.data)
        if serializer.is_valid():
            inst = serializer.save()
            clientnumber = request.data['number']

            mobile_number = clientnumber
            otp = randint(100000, 999999)

            try:
                client.messages.create(
                    body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
                    from_=twilio_phone,
                    to=mobile_number
                )
                ids = contactUS.objects.filter(number=clientnumber).last()
                enform = contactUS.objects.get(id = ids.id)
                enform.otp = str(otp)
                enform.save()
                return JsonResponse(status=202,data={'200':'Otp send successfully'})
            except TwilioRestException:
                return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})
        else:
            return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["POST"])
def resendCUotp(request):
    clientnumber = request.data.get('number')
    mobile_number = clientnumber
    otp = randint(100000, 999999)
    try:
        client.messages.create(
            body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
            from_=twilio_phone,
            to=str(mobile_number)
        )
        ids = contactUS.objects.filter(number=clientnumber).last()
        conform = contactUS.objects.get(id = ids.id)
        conform.otp = str(otp)
        conform.save()
        return JsonResponse(status=202,data={'200':'Otp send successfully'})
    except TwilioRestException:
        return JsonResponse(status=403,data={'403':'Mobile Number Invalid'})


@csrf_exempt
@api_view(["POST"])
def contactUSverify(request):
    mobile_number = request.data['mobile_number']
    otp = int(request.data['otp'])
    try:
        ids = contactUS.objects.filter(number=mobile_number).last()
        ef = contactUS.objects.get(id = ids.id)
    except:
        return JsonResponse(dict(detail="Wrong Mobile Number"))
    otp_timestamp = ef.createat.replace(tzinfo=None).timestamp()
    current_timestamp = datetime.datetime.now().timestamp()
    e = current_timestamp - otp_timestamp
    print("e",e)
    if e < 350:
        if otp == int(ef.otp):
            ef.is_verify = True
            ef.save()

            subject = 'Inquiry Request'
            message = f"Hi Admin \none candidate  Inquirey  \n user : {ef.name}, \n email : {ef.email},\n number : {ef.number}, \n course : {ef.course} "

            clientemail = 'info@aspirenowglobal.com'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [clientemail,]
            send_mail( subject, message, email_from, recipient_list)

            return JsonResponse(dict(detail="Verify Successfully "),status=200,)
        else:
            return JsonResponse(dict(detail="The provided code did not match "),status=401,)
    else:
        return JsonResponse(dict(detail="The provided code has expired"),status=401,)


def usersendmessage(name, email, contact):
    userc = User.objects.create(name=name, email=email, contact=contact, is_active=False)
    otp = randint(100000, 999999)
    try:
        client.messages.create(
            body="Please Enter This Otp " + str(otp) + " To Register at AspirenowGlobal",
            from_=twilio_phone,
            to=str(contact)
        )
        try:
            ids = Otp.objects.get(user_id=userc.id)
            ids.otpu = str(otp)
            ids.save()
        except Otp.DoesNotExist:
            Otp.objects.create(user_id=userc.id,otpu = str(otp))
        return JsonResponse(status=203,data={'203':'Otp send successfully'})
    except TwilioRestException:
        return JsonResponse(status=405,data={'403':'Mobile Number Invalid'})
    

@csrf_exempt 
@api_view(["POST"])
def UserPayment(request): 
    name = request.data['name']
    email = request.data['email']
    contact = request.data['contact']
    coursprice = int(request.data['coursprice'])
    coupan = request.data['coupan']
    coursename = request.data['coursename']

    courseid = Course.objects.get(title=coursename)
    try:
        userc = User.objects.get(contact=contact)
        try:
            userdata = User.objects.get(contact=contact, is_active=False)
            userdata.delete()
            data = usersendmessage(name, email, contact)
            return data
        except User.DoesNotExist:
                data = Purchase.objects.filter(purchaseuser_id = userc.id, cours_id=courseid).values('id').last()
                print("data",data)
                if data != None:
                    return JsonResponse(status=202,data={'msg':'You already purchase this course'})
                
    except User.DoesNotExist:
        data = usersendmessage(name, email, contact)
        return data

    try:
        ids = Student.objects.get(mobile=contact)
        stid = ids.id
        stp = StudentPercentage.objects.filter(student_id = stid, coupancode=coupan).values('percentag')
        if len(stp) != 0:
            strin = str(stp[0])
            f = strin.find(":")
            l = strin.find('}')
            stp = strin[f+3:l-1]
            if int(stp) >= 90:
                price = (coursprice // 100) * 25
                prices = coursprice - price
                return JsonResponse(dict(prices=prices, userid = userc.id, courseid= courseid.id),status=200)
            elif int(stp) >= 80:
                price = (coursprice // 100) * 20
                prices = coursprice - price
                return JsonResponse(dict(prices=prices, userid = userc.id, courseid= courseid.id),status=200)
            elif int(stp)  >= 70:
                price = (coursprice // 100) * 10
                prices = coursprice - price
                return JsonResponse(dict(prices=prices, userid = userc.id, courseid= courseid.id),status=200)     
            elif int(stp)  >= 60:
                price = (coursprice   // 100 ) *5
                prices = coursprice - price 
                return JsonResponse(dict(prices=prices, userid = userc.id, courseid= courseid.id),status=200)  
        else:
            return JsonResponse(dict(detail="This coupan Not Valid for your This Number",prices=coursprice, userid = userc.id, courseid= courseid.id),status=200,)
    except Student.DoesNotExist:
        return JsonResponse(dict(detail="You Not Give the exam",prices=coursprice, userid = userc.id, courseid= courseid.id),status=200,)


@csrf_exempt 
@api_view(["POST"])
def UserPaymentVerify(request): 
    otp = request.data['otp']
    contact = request.data['contact']
    coursprice = int(request.data['coursprice'])
    coupan = request.data['coupan']
    coursename = request.data['coursename']

    courseid = Course.objects.get(title=coursename)
    
    try:
        auth = Otp.objects.get(user=User.objects.get(contact=contact))
        old_date = auth.created_at
        old_date = old_date.replace(tzinfo=None).timestamp()
        current= datetime.datetime.now().timestamp()
        e = current - old_date
        if e > 350:
            auth.delete()
            return Response({"status": "Otp Expire"})
        else:
            if auth.otpu == otp:
                upassword = randint(10000000, 99999999)
                password = User.objects.get(contact=contact)
                password.set_password(str(upassword))
                password.is_active = True
                password.save()
                subject = 'Credentials'
                message = f"Thank you For Registering With Us \n Your Login Details For The Study Portal Is \nemail : {password.email}, Password : {upassword}"
                
                clientemail = password.email
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [clientemail,]
                send_mail( subject, message, email_from, recipient_list)

                try:
                    ids = Student.objects.get(mobile=contact)
                    stid = ids.id
                    stp = StudentPercentage.objects.filter(student_id = stid, coupancode=coupan).values('percentag')
                    if len(stp) != 0:
                        strin = str(stp[0])
                        f = strin.find(":")
                        l = strin.find('}')
                        stp = strin[f+3:l-1]
                        if int(stp) >= 90:
                            price = (coursprice // 100) * 25
                            prices = coursprice - price
                            return JsonResponse(dict(prices=prices, userid = password.id, courseid= courseid.id),status=200)
                        elif int(stp) >= 80:
                            price = (coursprice // 100) * 20
                            prices = coursprice - price
                            return JsonResponse(dict(prices=prices, userid = password.id, courseid= courseid.id),status=200)
                        elif int(stp)  >= 70:
                            price = (coursprice // 100) * 10
                            prices = coursprice - price
                            return JsonResponse(dict(prices=prices, userid = password.id, courseid= courseid.id),status=200)     
                        elif int(stp)  >= 60:
                            price = (coursprice   // 100 ) *5
                            prices = coursprice - price 
                            return JsonResponse(dict(prices=prices, userid = password.id, courseid= courseid.id),status=200)  
                    else:
                        return JsonResponse(dict(detail="This coupan Not Valid for your This Number",prices=coursprice, userid = password.id, courseid= courseid.id),status=200,)
                except Student.DoesNotExist:
                    return JsonResponse(dict(detail="You Not Give the exam",prices=coursprice, userid = password.id, courseid= courseid.id),status=200,)
            else:
                return Response({'status': 'Wrong Otp'},status=HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({"status": "Otp Expire"})

@csrf_exempt 
@api_view(["POST"])
def ConfirmPayment(request):
    paymentid = request.data['paymentid']
    userid = request.data['userid']
    courseid = request.data['courseid']
    amount = request.data['amount']

    data= os.popen(f"curl -X POST 'https://www.payumoney.com/payment/payment/chkMerchantTxnStatus?merchantKey=BQEALU8G&merchantTransactionIds={paymentid}' -H 'authorization: 3YGw9vDGsr81AINiu1h43qZmPWaJFKwsMWvtgbZiJ8I=' -H 'cache-control: no-cache'").read()
    res = json.loads(data)
    status = res['status']
    if status == 0:
        try:
            PaymentInfo.objects.get(paymentId=paymentid)
            return JsonResponse(dict(detail="Payment already exits",status=400,))
        except PaymentInfo.DoesNotExist:    
            PaymentInfo.objects.create(paymentId=paymentid, amount=amount, user_id = userid)
            userids = User.objects.get(id=userid)
            try:
                pk=Student.objects.get(mobile = userids.contact)
                try:
                    stp = StudentPercentage.objects.get(student_id =pk)
                    stp.coupancode = " "
                    stp.save()
                except StudentPercentage.DoesNotExist:
                    pass
            except Student.DoesNotExist:        
                pass
               

            for chid in Chapter.objects.filter(course_id = courseid).values('id'):
                pc = Purchase.objects.create(purchaseuser_id = userid, cours_id=courseid, chapter_id = int(chid['id']))
                for fc in FileUpload.objects.filter(chapter_id = int(chid['id'])).values('id'):
                    pc.media.add(int(fc['id']))
                    pc.save()
            return JsonResponse(dict(detail="Successful Payment",status=200,))
    else:
        return JsonResponse(dict(detail="Invalid Payment id",status=400,))

@csrf_exempt 
@api_view(["GET","POST"])
def topicepurget(request,pk):
    t = request.META['HTTP_AUTHORIZATION']
    currency = request.data['currency']
    userid=Token.objects.get(key=t)
    userid=int(userid.user.id)
    userids = User.objects.get(id=userid)
    chid = Chapter.objects.get(id = pk)
    if currency == "USD":
        prices = chid.priceusd
    else:
        prices = chid.price
    return JsonResponse(dict(detail="ok", email= userids.email,courseid=chid.course.id,chapterid =chid.id, name= userids.name, contact= userids.contact, topicename=chid.title, topiceprice=prices, status=200,))


@csrf_exempt 
@api_view(["POST"])
def topicepurchase(request):
    paymentid = request.data['paymentid']
    courseid = request.data['courseid']
    chapterid = request.data['chapterid']
    amount = request.data['amount']
    t = request.META['HTTP_AUTHORIZATION']
    userid=Token.objects.get(key=t)
    userid=int(userid.user.id)

    data= os.popen(f"curl -X POST 'https://www.payumoney.com/payment/payment/chkMerchantTxnStatus?merchantKey=BQEALU8G&merchantTransactionIds={paymentid}' -H 'authorization: 3YGw9vDGsr81AINiu1h43qZmPWaJFKwsMWvtgbZiJ8I=' -H 'cache-control: no-cache'").read()
    res = json.loads(data)
    status = res['status']
    if status == 0:
        try:
            PaymentInfo.objects.get(paymentId=paymentid)
            return JsonResponse(dict(detail="Payment already exits",status=400,))
        except PaymentInfo.DoesNotExist:    
            PaymentInfo.objects.create(paymentId=paymentid, amount=amount, user_id = userid)
            userids = User.objects.get(id=userid)
            chid = Chapter.objects.get(id = chapterid)
            pc = Purchase.objects.create(purchaseuser_id = userids.id, cours_id=courseid, chapter_id = chid.id)
            for fc in FileUpload.objects.filter(chapter_id = chid.id).values('id'):
                pc.media.add(int(fc['id']))
                pc.save()
            return JsonResponse(dict(detail="Successful Payment",status=200,))
    else:
        return JsonResponse(dict(detail="Invalid Payment id",status=400,))


class UserRU(generics.RetrieveAPIView,  mixins.DestroyModelMixin, mixins.UpdateModelMixin):
                              
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser,)
    def get_object(self):
        t = self.request.META['HTTP_AUTHORIZATION']
        userid=Token.objects.get(key=t)
        userid = userid.user.id
        obj = get_object_or_404(User, id=userid)
        return obj

    def put(self, request, *args, **kwargs): 
        return self.update(request, *args, **kwargs)


@csrf_exempt 
@api_view(["GET"])
def userlist(request):
    userinfo = User.objects.filter(is_active=True).values('id','email')
    return Response({'userinfo' : userinfo})


@csrf_exempt
@api_view(["POST"])
def fullcoursep(request):
    courseid = request.data['courseid']
    t = request.META['HTTP_AUTHORIZATION']
    currency = request.data['currency']
    userid=Token.objects.get(key=t)
    userid=int(userid.user.id)
    userid = User.objects.get(id=userid)
    pricec = Course.objects.get(id=courseid)
    if currency == "USD":
        prices = pricec.priceUSD
    else:
        prices = pricec.price
    return Response({'userid' : userid.id , 'username' : userid.name, 'useremail' : userid.email, 'userphone' : userid.contact, 'courseprice' : prices })


@csrf_exempt
@api_view(["POST"])
def coursepayment(request):
    paymentid = request.data['paymentid']
    userid = request.data['userid']
    courseid = request.data['courseid']
    amount = request.data['amount']
    print("amount", amount)
    data= os.popen(f"curl -X POST 'https://www.payumoney.com/payment/payment/chkMerchantTxnStatus?merchantKey=BQEALU8G&merchantTransactionIds={paymentid}' -H 'authorization: 3YGw9vDGsr81AINiu1h43qZmPWaJFKwsMWvtgbZiJ8I=' -H 'cache-control: no-cache'").read()
    res = json.loads(data)
    status = res['status']

    if status == 0:
        try:
            PaymentInfo.objects.get(paymentId=paymentid)
        except PaymentInfo.DoesNotExist:
            PaymentInfo.objects.create(paymentId=paymentid, amount=amount, user_id = userid)
        userids = User.objects.get(id=userid)
        for chid in Chapter.objects.filter(course_id = courseid).values('id'):
            pc = Purchase.objects.create(purchaseuser_id = userid, cours_id=courseid, chapter_id = int(chid['id']))
            for fc in FileUpload.objects.filter(chapter_id = int(chid['id'])).values('id'):
                pc.media.add(int(fc['id']))
                pc.save()
        return JsonResponse(dict(detail="Successful Payment",status=200,))

    else:
        return JsonResponse(dict(detail="Invalid Payment id",status=400,))


