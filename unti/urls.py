from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('api/get_trade_data.json', views.get_trade_data),
    path('api/get_brand_list.json', views.get_brand_list),
    path('api/test', views.test),
    path('api/get_trades_from_stooq', views.get_trades_from_stooq),
    path('api/get_brands_from_tse', views.get_brands_from_tse),

]
