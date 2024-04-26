from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
)
from django.urls import reverse


class Task(Model):
    title = CharField(max_length=50)  # type: ignore[var-annotated]
    description = CharField(max_length=250)  # type: ignore[var-annotated]
    created_at = DateTimeField(auto_now_add=True)  # type: ignore[var-annotated]
    due_at = DateTimeField(blank=True, null=True)  # type: ignore[var-annotated]
    is_completed = BooleanField(default=False)  # type: ignore[var-annotated]
    user = ForeignKey(get_user_model(), on_delete=CASCADE)  # type: ignore[var-annotated]

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self) -> str:
        return reverse("task", args=[self.pk])

    def __str__(self) -> str:
        return self.title
