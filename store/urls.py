
from django.contrib import admin
from django.urls import path , include

from . import views


urlpatterns = [

    path('',views.home,name='home'),
    path('about/',views.about_page,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_info/',views.update_info,name='update_info'),
    path('search_products/',views.search,name='search'),
    path('update_password/',views.update_password,name='update_password'),
    path('product/<int:pk>',views.product_view,name='product'),
    path('category/<str:cat>',views.category_view,name='category')
]
