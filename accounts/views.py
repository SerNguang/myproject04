from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, PhoneOTP
from django.shortcuts import get_object_or_404
import random

from .serializer import CreateUserSerializer

class ValidatePhoneSendOTP(APIView):
    
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'phone number already exist'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status': False,
                                'detail': 'Sending otp error. Limit exceeded.  Please contact customer support'
                            })
                        old.count = count + 1
                        old.save()
                        print("count increase", count)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully'
                        })
                    else:

                        PhoneOTP.objects.create(
                            phone = phone,
                            otp = key,
                        )
                        return Response({
                            'status': True,
                            'detail': "OTP sent successfully"                            
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Sending otp error'
                    })

        else:
            return Response({
                'status': False,
                'detail': 'Phone nuber is not given in post request'
            })

def send_otp(phone):
    if phone:
        key=random.randint(999,9999)
        print(key)
        return key

    else:
        return False


class ValidateOTP(APIView):
    """
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    """

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP MATCHED.  Please proceed for registration'
                    })

                else:
                    return Response({
                        'status': False,
                        'detail': "OTP INCORRECT"
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'First proceed via sending otp request'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validation'
            })

class Register(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        date_joined = request.data.get('date_joined', False)
        cea_reg = request.data.get('cea_reg', False)
        designation = request.data.get('designation', False)
        name = request.data.get('name', False)
        about_me = request.data.get('about_me', False)
        profile_image = request.data.get('profile_image', False)
        agency = request.data.get('agency', False)
        verified = request.data.get('verified', False)

        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old =  old.first()
                validated = old.validated

                if validated:
                    temp_data = {
                        'phone': phone,
                        'password': password,
                        'date_joined': date_joined,
                        'cea_reg': cea_reg,
                        'designation': designation,
                        'name': name,
                        'about_me': about_me,
                        'profile_image': profile_image
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception = True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'Account created'
                    })

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP haven verified yet.  First do that step'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Please verify phone first'
                })

        else:
            return Response({
                'status': False,
                'detail': 'Both phone and password are not sent'
            })