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
    return render(request, 'index.html')

def standings(request):
    # response = [
    #     [
    #         [
    #             {car.name, car.car}, {car.name, car.car}, {car.name, car.car}
    #         ],
    #         [
    #             {car.name, car.car}, {car.name, car.car}, {car.name, car.car}
    #         ]
    #     ],
    #     [
    #         [{car.name, car.car}, {car.name, car.car}, {car.name, car.car}],
    #         [{car.name, car.car}, {car.name, car.car}, {car.name, car.car}]
    #     ]
    # ]
    
    
    divs, cats, entries = Division.objects.all(), Category.objects.all().order_by('name'), []
    
    for d in divs:
        a = {d.name: []}
        for c in cats:
            b = {c.name: []}
            ps = Poll.objects.filter(division=d, category=c).order_by('-votes')[:3]
            if len(ps) > 0:
                for thing in ps:
                    b[c.name].append({"name":thing.car.owner_name, "car":thing.car.car})
                a[d.name].append(b)
        entries.append(a)
    print(entries)
    # for d in divs:

    #     for c in cats:

    #         data = Poll.objects.filter(division=d, category=c).order_by('-votes')[:3]
    #         for item in data:
            #     if Division.objects.get(pk=item.division_id).name not in divs:
            #         divs.append(Division.objects.get(pk=item.division_id.name))
            #     if Category.objects.get(pk=item.category_id).name not in cats:
            #         cats.append(Category.objects.get(pk=item.category_id).name)
                # obj = {}
                # entry = Car.objects.get(pk=item.car_id)
                # obj['name'] = entry.owner_name
                # obj['car'] = entry.car
                # obj['category'] = Category.objects.get(pk=item.category_id).name
                # obj['division'] = Division.objects.get(pk=item.division_id).name
                # obj['votes'] = item.votes
                # obj['poll_id'] = item.id
                # entries.append(obj)

    # for d in Division.objects.all():
    #     for c in Category.objects.all():
    #         ps = Poll.objects.filter(division=d, category=c).order_by('-votes')
    return JsonResponse({"entries":entries}, safe=False)
        

def get_divisions(request):
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





