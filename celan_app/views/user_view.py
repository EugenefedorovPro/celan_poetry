from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_205_RESET_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from celan_app.serializers.user_serializer import SignupSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"message": f"something gets wrong with error: {e}"},
                status=HTTP_400_BAD_REQUEST,
            )
