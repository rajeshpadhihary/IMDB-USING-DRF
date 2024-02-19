from .models import *
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from .models import Users
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes([AllowAny])
def Register_Users(request):
    try:
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            return Response(
                {
                    "token": token,
                    "message": f"Hii {account.name} you are registered successfully. Having Email_Id : {account.Email_Address}",
                }
            )

        else:
            data = serializer.errors

        return Response(data)
    except IntegrityError as e:
        account = Users.objects.get(name="")
        account.delete()
        raise ValidationError({"400": f"{str(e)}"})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f"Field {str(e)} missing"})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    reqBody = json.loads(request.body)
    email1 = reqBody["Email_Address"]
    # print(email1)
    password = reqBody["password"]
    try:
        Account = Users.objects.get(Email_Address=email1)
    except BaseException as e:
        raise ValidationError({"400": f"{str(e)}"})

    token = Token.objects.get_or_create(user=Account)[0].key
    # print(token)
    if not check_password(password, Account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})

    if Account:
        if Account.is_active:
            login(request, Account)
            request.user.is_online = True
            request.user.save()
            data["message"] = f"Hey {Account.name} you are logged in"
            data["Email_Address"] = Account.Email_Address

            Res = {"data": data, "token": token}

            return Response(Res)

        else:
            raise ValidationError({"400": f"Account not active"})

    else:
        raise ValidationError({"400": f"Account doesnt exist"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    request.user.is_online = False
    request.user.save()
    logout(request)
    

    return Response({
        "logoutStatus":f"User Logged out successfully"
    })
