from django.urls import  path
from .views import TaskList, TaskDetails, TaskCreate, TaskUpdate, TaskDelete, UserLogin, UserRegister, UserList,  UserProfile, Test
from django.contrib.auth.views import LogoutView



urlpatterns = [

    path('login/', UserLogin.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(next_page = 'login'), name='logout' ),
    path('register/', UserRegister.as_view(), name='register' ),

    path('users/', UserList.as_view(), name='users' ),
    
    path('task/', TaskList.as_view(), name='tasks' ),
    path('task/<int:pk>/', TaskDetails.as_view(), name='task' ),
    path('task/create/', TaskCreate.as_view(), name='task-create' ),
    path('task/update/<int:pk>/', TaskUpdate.as_view(), name='task-update' ),
    path('task/Delete/<int:pk>/', TaskDelete.as_view(), name='task-delete' ),
    path('users/profile/<int:pk>/', UserProfile.as_view(), name='profile' ),
    path('taskk/', Test.as_view(), name='taskk' ),
    
]