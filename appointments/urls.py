from django.urls import path
from .views import AppointmentView,  AppointView
app_name = 'appointments'

urlpatterns = [
        path('', AppointmentView.as_view(), name='make_appointment'),
        path('appoint/', AppointView.as_view(), name='test'),
]