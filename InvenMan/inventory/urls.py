from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.projecthomepage,name='projecthomepage'),
    path('add-item/', views.add_item, name='add_item'),
    path('view-items/', views.view_items, name='view_items'),
    path('login1/<int:item_id>/', views.login1, name='login1'),
    path('login2/<int:item_id>/', views.login2, name='login2'),
    path('login3/', views.login3, name='login3'),
    path('login4/', views.login4, name='login4'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('borrow-item/', views.borrow_item, name='borrow_item'),
    path('borrowed-items/', views.borrowed_items, name='borrowed_items'),
    path('mark_returned/<int:borrower_id>/', views.mark_returned, name='mark_returned'),


]