from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.plot_sales, name='home'),
    path('login', views.view_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('do_logout', views.do_logout, name='do_logout'),
    path('list', views.list, name='list'),
    path('add', views.add, name='add'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('view_delete', views.view_delete, name='view_delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('sale', views.sale, name='sale'),
    path('sale_list', views.sale_list, name='sale_list'),
    path('reorder', views.reorder, name='reorder'),
]