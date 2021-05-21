from django.urls import path,include
from .views import index,home,success
urlpatterns = [
    path('', index,name="index"),
    path('home',home,name="home"),
    path('success',success,name="success")
]