from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('api/index.json', views.index),
    path('api/get_brand_list.json', views.get_brand_list),
]
