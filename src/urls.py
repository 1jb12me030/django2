from django.contrib import admin
from django.urls import path
from src.views import coffee_payment,payment_status

urlpatterns = [
    path('', coffee_payment ,name='coffee-payment'),
    #path('register',register_attempt,name='register_attempt'),
    path('payment-status', payment_status ,name='payment-status')

]