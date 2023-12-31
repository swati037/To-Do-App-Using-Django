from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    
    path('todo_list/', views.todo_list, name='todo_list'),
    path('create_task/', views.create_task, name='create_task'),
    path('update_task/<int:pk>/', views.update_task, name='update_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    
    path('logout/', views.logout_view, name='logout'),
    # path('welcome/<str:username>/', views.welcome_view, name='welcome'),
]


# handler404 = 'todo.views.page_not_found'