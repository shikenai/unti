from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('api/get_trade_data.json', views.get_trade_data),
    path('api/get_brand_list.json', views.get_brand_list),
]
