from django.urls import path

from . import views

urlpatterns = [

    path('', views.summary, name='cart_summary'),
    path('delete/', views.delete, name='delete_cart'),
    path('add/', views.add, name='add_cart'),
    path('update/', views.update, name='update_cart'),

]
