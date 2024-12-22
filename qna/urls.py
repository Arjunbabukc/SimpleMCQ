from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enter_name/', views.enter_name, name='enter_name'),
    path('results/', views.results, name='results'),  # Ensure this is correct
]
