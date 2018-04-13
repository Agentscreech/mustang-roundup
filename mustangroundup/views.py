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
    categories = []
    for item in data:
        obj = {}
        entry = Car.objects.get(pk=item.car_id)
        obj['name'] = entry.owner_name
        obj['car'] = entry.car
        if Category.objects.get(pk=item.category_id).name not in categories:
            categories.append(Category.objects.get(pk=item.category_id).name)
        obj['category'] = Category.objects.get(pk=item.category_id).name
        obj['votes'] = item.votes
        obj['poll_id'] = item.id
        entries.append(obj)

    return JsonResponse([entries, sorted(categories)], safe=False)

def update_poll(request, id):
    try:
        poll = Poll.objects.get(pk=id)
        poll.votes += 1
        poll.save()
        return HttpResponse("poll updated")
    except:
        return HttpResponse("error happened")





