
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls'), name='login'),
    path("", include("users.urls"), name='main'),
    path("api/v1/fridge/", include('fridge.urls'), name='fridge'),
]
