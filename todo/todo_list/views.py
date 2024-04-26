from datetime import UTC, datetime

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from todo_list.forms import TaskForm
from todo_list.models import Task


class TasksView(ListView):
    template_name = "todo_list/tasks.html"
    model = Task
    paginate_by = 5
    context_object_name = "tasks"


class TaskView(DetailView):
    template_name = "todo_list/task.html"
    model = Task
    context_object_name = "task"
    pk_url_kwarg = "id"


class CreateTask(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_list/create_task.html"

    def get_success_url(self) -> str:
        assert self.object is not None
        return reverse("task", args=[self.object.pk])


@require_POST
def complete_task(request: HttpRequest, id: int) -> HttpResponseRedirect:
    task = get_object_or_404(Task, id=id)
    task.is_completed = True
    task.due_at = datetime.now(UTC)
    task.save()
    return redirect("task", id=id)


class DeleteTask(DeleteView):
    model = Task
    pk_url_kwarg = "id"
    success_url = reverse_lazy("index")
