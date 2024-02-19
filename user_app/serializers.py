from rest_framework import serializers
from .models import Users

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = [
            "name",
            "Email_Address",
            "zipcode",
            "Date_of_Birth",
            "password",

        ]
    def create(self, validated_data):
        extra_kwargs = {"password": {"write_only": True}}
        password = validated_data["password"]
        Email_Address = validated_data['Email_Address']
        name = validated_data['name']
        birthday = validated_data['Date_of_Birth']
        zipcode = validated_data['zipcode']
        account = Users.objects.create_user(Email_Address = Email_Address,name = name,birthday=birthday,zipcode=zipcode)
        account.set_password(password)
        account.save()
        return account