from django.urls import path, include, re_path
from django.contrib import admin
from . import views
# from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# urlpatterns = router.urls



urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('obtain-auth-token/', csrf_exempt(obtain_auth_token)),
    path('getDivisions/', views.get_divisions, name="get_divisions"),
    path('division/<division>/', views.division, name="division"),
    path('poll/<id>/', csrf_exempt(views.update_poll), name="update_poll"),
    path('standings/', views.standings, name="standings"),
    path('show_public/', views.show_public, name="show_public"),
    path('toggle_show/', csrf_exempt(views.toggle_show), name="toggle_show"),
    re_path(r'^.*/$', views.index, name="index")

]
