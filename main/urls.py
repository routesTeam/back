from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generator/', views.generator, name='generator'),
    path('testgen/', views.testgen, name='testgen'),
]