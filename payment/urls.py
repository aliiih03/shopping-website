from django.urls import path

from . import views

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('process_order', views.process_order, name='process_order'),
    path('shipped_order', views.shipped_order, name='shipped_order'),
    path('not_shipped_order', views.not_shipped_order, name='not_shipped_order'),
    path("orders/<int:pk>/", views.orders, name="orders"),
]
