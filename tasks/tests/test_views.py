from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.forms import TaskForm, RemoveTagForm
from tasks.models import Task, Tag


TASK_URL = reverse("tasks:index")
TAG_URL = reverse("tasks:tags")
TASK_CREATE_URL = reverse("tasks:task_create")


class TasksViewsTests(TestCase):
    def test_task_view_status_code(self) -> None:
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_tasks(self) -> None:
        Task.objects.create(
            content="Task1",
            deadline=timezone.now()
        )
        Task.objects.create(
            content="Task2",
            deadline=timezone.now()
        )
        res = self.client.get(TASK_URL)
        tasks = Task.objects.all().order_by("-id")
        self.assertEqual(list(res.context["tasks"]), list(tasks))

    def test_task_list_view_template_used(self) -> None:
        res = self.client.get(TASK_URL)
        self.assertTemplateUsed(res, "tasks/task_list.html")

    def test_change_status_done(self) -> None:
        task = Task.objects.create(
            content="Task",
            deadline=timezone.now()
        )
        self.assertFalse(task.is_done)
        change_status_url = reverse("tasks:task_change-status", args=[task.id])
        self.client.get(change_status_url)
        task.refresh_from_db()
        self.assertTrue(task.is_done)
        res = self.client.get(change_status_url)
        task.refresh_from_db()
        self.assertFalse(task.is_done)
        self.assertRedirects(res, reverse("tasks:index"))

    def test_change_status_404(self) -> None:
        change_status_url = reverse("tasks:task_change-status", args=[999])
        res = self.client.get(change_status_url)
        self.assertEqual(res.status_code, 404)

    def test_task_create_view_status_code(self) -> None:
        res = self.client.get(TASK_CREATE_URL)
        self.assertEqual(res.status_code, 200)

    def test_task_create_success(self) -> None:
        data = {
            "content": "Task",
            "deadline": timezone.now()
        }
        response = self.client.post(TASK_CREATE_URL, data)
        self.assertRedirects(response, TASK_URL)
        task = Task.objects.get(content="Task")
        self.assertEqual(task.content, "Task")

    def test_create_view_uses_correct_form(self) -> None:
        response = self.client.post(TASK_CREATE_URL)
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_task_create_view_template_used(self) -> None:
        res = self.client.get(TASK_CREATE_URL)
        self.assertTemplateUsed(res, "tasks/task_form.html")


class TaskRemoveTagTests(TestCase):
    def setUp(self) -> None:
        self.task = Task.objects.create(
            content="Test task",
            deadline=timezone.now()
        )
        self.tag1 = Tag.objects.create(name="Test tag 1")
        self.tag2 = Tag.objects.create(name="Test tag 2")
        self.task.tags.set([self.tag1, self.tag2])
        self.url = reverse(
            "tasks:task-remove-tag",
            kwargs={"pk": self.task.pk}
        )

    def test_get_task_remove_tag_view(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_remove_tag.html")
        self.assertIsInstance(response.context["form"], RemoveTagForm)
        self.assertIn(self.tag1, response.context["tags"])
        self.assertIn(self.tag2, response.context["tags"])

    def test_post_task_remove_tag_valid(self) -> None:
        data = {"tag": self.tag1.pk}
        response = self.client.post(self.url, data)

        self.task.refresh_from_db()
        self.assertNotIn(self.tag1, self.task.tags.all())
        self.assertIn(self.tag2, self.task.tags.all())

        self.assertRedirects(response, reverse("tasks:index"))


class TaskAddTagViewTests(TestCase):
    def setUp(self) -> None:
        self.task = Task.objects.create(
            content="Test task",
            deadline=timezone.now()
        )
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")
        self.url = reverse("tasks:task-add-tag", args=[self.task.id])

    def test_get_add_tag_view(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tasks/task_add_tag.html")
        self.assertEqual(response.context["task"], self.task)
        self.assertIn("form", response.context)
        tags = response.context["tags"]
        self.assertIn(self.tag1, tags)
        self.assertIn(self.tag2, tags)

    def test_post_add_tag_view_valid(self) -> None:
        valid_data = {"tag": self.tag1.id}
        response = self.client.post(self.url, data=valid_data)
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertIn(self.tag1, self.task.tags.all())


class TagsViewsTests(TestCase):
    def test_tag_view_status_code(self) -> None:
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_tag(self) -> None:
        Tag.objects.create(name="Tag1")
        Tag.objects.create(name="Tag2")
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all()
        self.assertEqual(list(res.context["tags"]), list(tags))

    def test_tag_list_view_template_used(self) -> None:
        res = self.client.get(TAG_URL)
        self.assertTemplateUsed(res, "tasks/tag_list.html")


class TagCreateTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse("tasks:tag_create")

    def test_create_tag_valid_data(self) -> None:
        data = {"name": "New Tag"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, "New Tag")


class TagUpdateTests(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="Old Tag")
        self.url = reverse("tasks:tag_update", args=[self.tag.id])

    def test_update_tag_valid_data(self) -> None:
        data = {"name": "Updated Tag"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated Tag")


class TagDeleteTests(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="Tag to Delete")
        self.url = reverse("tasks:tag_delete", args=[self.tag.id])

    def test_delete_tag(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 0)
