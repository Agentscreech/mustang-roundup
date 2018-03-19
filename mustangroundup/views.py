from django.shortcuts import render, redirect
from rest_framework import viewsets, response, permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)

def index(request):
  return render(request, 'index.html')

def test(request):
    print(request.body)
    return render(request, 'index.html')





