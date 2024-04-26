from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from todo_list.models import Task


class TestTodoList(TestCase):
    def test_index_empty(self) -> None:
        index_url = reverse("index")

        response = self.client.get(index_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "todo_list/tasks.html")
        self.assertQuerysetEqual(response.context["tasks"], Task.objects.none())

    def test_index_not_empty(self) -> None:
        index_url = reverse("index")

        task = Task.objects.create(title="Title", description="Description")
        response = self.client.get(index_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "todo_list/tasks.html")
        self.assertEqual(len(response.context["tasks"]), 1)
        self.assertEqual(response.context["tasks"][0], task)

    def test_task_not_found(self) -> None:
        task_url = reverse("task", args=[1])

        response = self.client.get(task_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_task_found(self) -> None:
        task = Task.objects.create(title="Title", description="Description")
        task_url = reverse("task", args=[task.pk])

        response = self.client.get(task_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "todo_list/task.html")
        self.assertEqual(response.context["task"], task)

    def test_render_create_task_form(self) -> None:
        create_task_url = reverse("create-task")

        response = self.client.get(create_task_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "todo_list/create_task.html")

    def test_create_task_redirect(self) -> None:
        create_task_url = reverse("create-task")
        task_url = reverse("task", args=[1])

        response = self.client.post(create_task_url, data={"title": "Title", "description": "Description"})

        self.assertRedirects(response, expected_url=task_url)

    def test_create_task_invalid_data(self) -> None:
        create_task_url = reverse("create-task")

        response = self.client.post(create_task_url, data={"title": "Title"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "todo_list/create_task.html")

    def test_complete_task(self) -> None:
        task = Task.objects.create(title="Title", description="Description")
        task_url = reverse("task", args=[task.pk])
        complete_task_url = reverse("complete-task", args=[task.pk])

        self.assertFalse(task.is_completed)

        response = self.client.post(complete_task_url)

        self.assertRedirects(response, expected_url=task_url)

        task = Task.objects.get(pk=task.pk)

        self.assertTrue(task.is_completed)

    def test_delete_task(self) -> None:
        task = Task.objects.create(title="Title", description="Description")
        index_url = reverse("index")
        delete_task_url = reverse("delete-task", args=[task.pk])

        response = self.client.post(delete_task_url)

        self.assertRedirects(response, expected_url=index_url)

        task_url = reverse("task", args=[task.pk])

        response = self.client.get(task_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
