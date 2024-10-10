from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from tasks.models import Task, Tag


class TodoList(LoginRequiredMixin, generic.ListView):
    context_object_name = "tasks"
    template_name = "tasks/todo_list.html"

    def get_queryset(self):
        return Task.objects.order_by("is_done", "-date_of_create")


class TagList(LoginRequiredMixin, generic.DetailView):
    model = Tag
