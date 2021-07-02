from django.urls import path, include

from reports import views

urlpatterns = [
    path('', views.index, name='index'),
]
