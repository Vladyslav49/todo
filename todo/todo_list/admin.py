from django.contrib import admin
from django.contrib.admin import ModelAdmin

from todo_list.models import Task


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    readonly_fields = ["created_at"]
