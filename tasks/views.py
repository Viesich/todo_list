from django.views import generic
from django.urls import reverse_lazy

from tasks.models import Task, Tag


class TodoList(generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/todo_list.html"

    def get_queryset(self):
        return Task.objects.order_by("is_done", "-date_of_create")


class TagList(generic.ListView):
    model = Tag
    context_object_name = "tags"
    template_name = "tasks/tag_list.html"

    def get_queryset(self):
        return Tag.objects.all()


class TagCreate(generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tags")
    template_name = "tasks/tag_form.html"


class TagUpdate(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tags")
    template_name = "tasks/tag_form.html"


class TagDelete(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tags")
    template_name = "tasks/tag_confirm_delete.html"

