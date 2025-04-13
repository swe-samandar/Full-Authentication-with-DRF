from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import CustomUser


def validate_phone_number(phone_):
    """Telefon raqam validatsiyadan o'tsa True qaytaradi"""
    phone = str(phone_)
    return len(phone) == 12 and isinstance(phone_, int) and phone[:3] == '998'

def validate_password(password):
    """Parol validatsiyadan o'tsa True qaytaradi"""
    return 6 <= len(password) <= 128 and any(map(lambda x:x.isupper(), password)) and any(map(lambda x:x.islower(), password)) and ' ' not in password

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        data = request.data

        # Telefon raqam va password kiritlganligini tekshiruvchi shartli qism
        if 'phone' not in data or 'password' not in data:
            return Response(
                {'Message': 'Telefon raqam yoki parol kiritilmagan.'},
                status=status.HTTP_400_BAD_REQUEST
                )

        # Telefon raqamni validatsiyadan o'tkazish
        if not validate_phone_number(data['phone']):
            return Response(
                {"Message": 'Telefon raqamni tekshirib qaytadan kiriting.'},
                status=status.HTTP_400_BAD_REQUEST
                )

        # Avval bu telefon raqam orqali ro'yxatdan o'tilmaganligini tekshiruvchi shartli qism
        phone = CustomUser.objects.filter(phone=data['phone']).first()
        if phone:
            return Response(
                {'Message': 'Bu telefon raqam bilan avval ro\'yxatdan o\'tilgan'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # Parolni validatsiyadan o'tkazadi
        if not validate_password(data['password']):
            return Response(
                {"Message": 'Parol talabga javob bermaydi, boshqa parol kiriting.'},
                status=status.HTTP_400_BAD_REQUEST
                )

        # Yuqoridagi shartlarni qanoatlantirgach foydalanuvchi ma'lumotlarini user_data nomli o'zgaruvchiga tenglashtirib oladi
        user_data = {
            'phone': data['phone'],
            'password': data['password'],
            'name': data.get('name', '')
            }

        # Agar `key'   `123` qiymatiga teng bo'lsa user_data ni yangilaydi
        if data.get('key', '') == '123':
            user_data.update({
                'is_staff': True,
                'is_superuser': True
            })
        
        # `key` yuborilmagan holatda yoki noto'g'ri `key` yuborilgan holatda oddiy foydalanuvchi yaratiladi
        user = CustomUser.objects.create_user(**user_data)
        Token.objects.create(user=user)
        return Response(
            {
                'Message':"Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
                'is_superuser': user_data.get('is_superuser', False),
                'token': user.auth_token.key
                },
            status=status.HTTP_201_CREATED
            )
    

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = CustomUser.objects.filter(phone=data['phone']).first()

        if not user:
            return Response(
                {'Error': "Bu telefon raqam bilan ro'yxatdan o'tilmangan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(data['password']):
            return Response(
                {'Error': "Noto'g'ri parol kiritildi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = Token.objects.get_or_create(user=user)

        return Response(
            {
                'Message': 'Siz tizimga muvaffaqiyatli kirdingiz.',
                'token': token[0].key
                },
            status=status.HTTP_200_OK
        )
    
    
class LogoutView(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,
    
    def post(self, request):
        token = Token.objects.filter(user=request.user).first()
        token.delete()
        return Response(
            {'Message': 'Siz tizimdan chiqarildingiz.'}, 
            status=status.HTTP_200_OK
            )


class ProfileView(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,

    # Foydalanuvchining [phone, name, is_active, is_staff, is_superuser] ma'lumotlarini qaytaradi
    def get(self, request):
        user = request.user
        return Response(
            {'Data': user.format()},
            status=status.HTTP_200_OK
            )
 
    def patch(self, request):
        """
        Foydalanuvchining telefon nomeri va ismini o'zgartiradi, 
        agar data `key` berilsa va u to'g'ri bo'lsa superuser ga o'zgartiriladi
        """
        data = request.data
        user = request.user

        if not data.get('phone', ''):
            return Response(
                {'Error': 'Telefon raqam kiritlishi shart.'},
                status=status.HTTP_400_BAD_REQUEST
                )

        if not validate_phone_number(data['phone']):
            return Response(
                {"Error": 'Telefon raqamni tekshirib qaytadan kiriting.'},
                status=status.HTTP_400_BAD_REQUEST
                )
       
        # data['phone'] = str(data['phone'])
        user_ = CustomUser.objects.filter(phone=data['phone']).first()

        if user_ and user != user_:
            return Response(
                {'Message': "Bu raqam bilan avvalroq ro'yxatdan o'tilgan."},
                status=status.HTTP_400_BAD_REQUEST
                )

        if data.get('key', '') == '123':
            user.is_staff = True
            user.is_superuser = True

        user.phone = data['phone']
        user.name = data.get('name', user.name)
        
        user.save()
        return Response(
            {
                'Message': "Ma'lumotlaringiz muvvaqiyatli o'zgartirildi.",
                'Data': f"O'zgartirilgan ma'lumotlar {data}",
                },
                status=status.HTTP_200_OK
            )

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {'Message': 'Telefon raqamingiz hisobdan chiqarildi.'},
            status=status.HTTP_200_OK
        )


class PasswordChangeView(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,

    def post(self, request):
        data = request.data
        user = request.user

        if not data.get('old') or not data.get('new'):
            return Response(
                {"Messages": 'Eski yoki yangi parol kiritilmagan.'},
                status=status.HTTP_400_BAD_REQUEST
                )

        if not user.check_password(data['old']):
            return Response(
                {"Error": "Eski parol noto'g'ri kiritilgan."},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        if not validate_password(data['new']):
            return Response(
                {"Message": 'Parol talabga javob bermaydi, boshqa parol kiriting.'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        user.set_password(data['new'])
        user.save()
        return Response(
            {'Message': "Parolingiz muvaffaqiyatli o'zgartirildi!"},
            status=status.HTTP_200_OK
            )