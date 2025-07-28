from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('signup/', views.Signup, name="sign-up"),
    path('task/', views.Tasks, name="tasks"),
    path('completed', views.TasksCompleted, name="task-completed"),
    path('logout/',views.Signout, name="log-out"),
    path('login/',views.Signin, name="login"),
    path('task/create', views.CreateTask, name="create-task"),
    path('task/<int:task_id>/', views.TaskDetail, name="task-detail"),
    path('task/<int:task_id>/complete', views.TaskComplete, name="task-complete"),
    path('task/<int:task_id>/delete', views.TaskDelete, name="task-delete"),
]
