from django.urls import path, include, re_path
from django.contrib import admin
from . import views
# from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls



urlpatterns += [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('obtain-auth-token/', csrf_exempt(obtain_auth_token)),
    # path('test/', csrf_exempt(views.test), name="test"),
    path('getDivisions/', views.get_divisions, name="get_divisions"),
    path('division/<division>/', views.division, name="division"),
    path('poll/<id>/', csrf_exempt(views.update_poll), name="update_poll"),
    re_path(r'^.*/$', views.index, name="index")
    # path('users/', UserViewSet)

    # path('api-auth/', include('rest_framework.urls'))

]
