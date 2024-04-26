from django.urls import path

from todo_list import views

urlpatterns = [
    path("", views.TasksView.as_view(), name="index"),
    path("task/<int:id>", views.TaskView.as_view(), name="task"),
    path("create_task/", views.CreateTask.as_view(), name="create-task"),
    path("complete_task/<int:id>", views.complete_task, name="complete-task"),
    path(
        "delete_task/<int:id>", views.DeleteTask.as_view(), name="delete-task"
    ),
]
