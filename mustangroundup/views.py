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

def get_divisions(request):
    print("getting divisions")
    data = Division.objects.all()
    names = []
    for obj in data:
        names.append(obj.name)
    return JsonResponse(names, safe=False)

def division(request, division):
    data = Poll.objects.filter(
        division_id=Division.objects.get(name=division).id
    )
    entries = []
    for item in data:
        obj = {}
        entry = Car.objects.get(pk=item.car_id)
        obj['name'] = entry.owner_name
        obj['car'] = entry.car
        obj['category'] = Category.objects.get(pk=item.category_id).name
        obj['votes'] = item.votes
        obj['poll_id'] = item.id
        entries.append(obj)
    
    return JsonResponse(entries, safe=False)

def update_poll(request, id):
    try:
        poll = Poll.objects.get(pk=id)
        poll.votes += 1
        poll.save()
        return HttpResponse("poll updated")
    except:
        return HttpResponse("error happened")

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
    




