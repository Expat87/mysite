from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pipe_data_sch', views.pipe_data_sch, name='pipe_data_sch'),
    path('pipe_data_flange', views.pipe_data_flange, name='pipe_data_flange'),

]
