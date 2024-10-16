from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render

from tasks.forms import TaskForm, AddTagForm, RemoveTagForm
from tasks.models import Task, Tag


class TaskList(generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        return Task.objects.order_by("is_done", "-date_of_create")


def change_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.is_done:
        task.is_done = False
    else:
        task.is_done = True
    task.save()
    return redirect("tasks:index")


class TaskCreate(generic.CreateView):
    model = Task
    form_class = TaskForm

    success_url = reverse_lazy("tasks:index")
    template_name = "tasks/task_form.html"


class TaskAddTag(generic.View):
    template_name = "tasks/task_add_tag.html"
    success_url = reverse_lazy("tasks:index")

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = AddTagForm()
        tags = Tag.objects.exclude(tasks=task)
        context = {
            "task": task,
            "form": form,
            "tags": tags,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = AddTagForm(request.POST)

        if form.is_valid():
            tag = form.cleaned_data["tag"]
            task.tags.add(tag)
            task.save()
            return redirect(self.success_url)

        tags = Tag.objects.all()
        context = {
            "task": task,
            "form": form,
            "tags": tags,
        }
        return render(request, self.template_name, context)


class TaskRemoveTag(generic.View):
    template_name = "tasks/task_remove_tag.html"
    success_url = reverse_lazy("tasks:index")

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = RemoveTagForm()
        tags = task.tags.all()
        context = {
            "task": task,
            "form": form,
            "tags": tags,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = RemoveTagForm(request.POST)

        if form.is_valid():
            tag = form.cleaned_data["tag"]
            task.tags.remove(tag)
            task.save()
            return redirect(self.success_url)

        tags = task.tags.all()
        context = {
            "task": task,
            "form": form,
            "tags": tags,
        }
        return render(request, self.template_name, context)


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
