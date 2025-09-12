from .models import User
from rest_framework import serializers
from django.core.validators import RegexValidator
from datetime import date
import base64


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[
        ('customer', 'Customer'),
        ('driver', 'Driver')
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message="Card number must be 16 digits."
            )
        ]
    )
    cvv = serializers.CharField(
        write_only=True, required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{3}$',
                message="CVV must be 3 digits."
            )
        ]
    )
    expiry_date = serializers.DateField(
        write_only=True,
        required=False,
        input_formats=['%m/%y']  # MM/YY format
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number', 'address', 'card_number', 'expiry_date', 'cvv']
        read_only_fields = ['username', 'email', 'role']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        card_number = validated_data.get('card_number')
        expiry_date = validated_data.get('expiry_date')
        cvv = validated_data.get('cvv')

        if card_number and expiry_date and cvv:
            month = expiry_date.month
            year = expiry_date.year
            today = date.today()
            if year < today.year or (year == today.year and month < today.month):
                raise serializers.ValidationError( "Card is expired.")
            
            try:
                merged = " ".join([cvv, str(month), str(year), card_number])
                encoded = int.from_bytes(merged.encode('utf-8'), 'big')
                # store fake_token in pyment_info for now
                instance.payment_info = encoded 

            except Exception as e:
                raise serializers.ValidationError({"payment_info": str(e)})
        instance.save()
        return instance