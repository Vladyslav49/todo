from datetime import UTC, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from todo_list.forms import TaskForm
from todo_list.models import Task


class TasksView(LoginRequiredMixin, ListView):
    template_name = "todo_list/tasks.html"
    model = Task
    paginate_by = 5
    context_object_name = "tasks"

    def get_queryset(self) -> QuerySet[Task]:
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)  # type: ignore[attr-defined]


class TaskView(LoginRequiredMixin, DetailView):
    template_name = "todo_list/task.html"
    model = Task
    context_object_name = "task"
    pk_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[Task]:
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo_list/create_task.html"

    def form_valid(self, form: TaskForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        assert self.object is not None
        return reverse("task", args=[self.object.pk])


@require_POST
@login_required
def complete_task(request: HttpRequest, id: int) -> HttpResponseRedirect:
    task = get_object_or_404(Task, pk=id, user=request.user)
    task.is_completed = True
    task.due_at = datetime.now(UTC)
    task.save()
    return redirect("task", id=id)


class DeleteTask(LoginRequiredMixin, DeleteView):  # type: ignore[misc]
    model = Task
    pk_url_kwarg = "id"
    success_url = reverse_lazy("index")

    def get_queryset(self) -> QuerySet[Task]:
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
