from django.shortcuts import render, redirect
from django.core import serializers
from rest_framework import viewsets, response, permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Poll, Division, Car, Category
from django.http import JsonResponse, HttpResponse
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
    # print("index firing")
    return render(request, 'index.html')

def test(request):
    data = Poll.objects.filter(
        division_id=Division.objects.get(name="Concourse Trailered").id)
    test = []
    for item in data:
        thing = {}
        entry = Car.objects.get(pk=item.car_id)
        thing['name'] = entry.owner_name
        thing['car'] = entry.car
        thing['category'] = Category.objects.get(pk=item.category_id).name
        test.append(thing)
    # parsed = serializers.serialize('json', test)
    print("test function firing")
    # test = Poll.objects.all()
    print(test)
    return JsonResponse(test, safe=False)
    




