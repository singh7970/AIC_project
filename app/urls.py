from django.contrib import admin
from django.urls import path
from .import views
from .views import patient_list

urlpatterns = [
    path("",views.index,name="index"),
    path('api/patients/', views.patient_list, name='patient-list'),
    #  path('', views.submit_form_view, name='submit_form'),

]


# http://aic4591q.com/
# https://secure12.oncoemr.com/nav/demographics?locationId=LH_Cz108527942_27