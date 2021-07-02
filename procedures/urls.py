from django.contrib import admin
from django.urls import path, include

from procedures import views
from procedures.views import load_file

urlpatterns = [
    path('', views.home, name='home'),
    path('lots_chart/', views.lots_chart, name='lots_chart'),
    path('data_by_curators/', views.data_by_curators, name='data_by_curators'),
    path('procedures/', views.ProcedureListView.as_view()),
    path('load_lots/', views.ProcedureCreate.as_view()),
    path('upload_lots/', load_file),
]
