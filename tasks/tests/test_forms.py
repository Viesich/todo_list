from django.test import TestCase
from django.utils import timezone
from tasks.forms import TaskForm, AddTagForm, RemoveTagForm
from tasks.models import Task, Tag


class TaskFormTests(TestCase):
    def setUp(self) -> None:
        tag1 = Tag.objects.create(name="test1")
        tag2 = Tag.objects.create(name="test2")

        self.task = Task.objects.create(
            content="Test Task",
            date_of_create=timezone.make_aware(timezone.datetime(2024, 10, 15, 12, 0, 0)),
            deadline=timezone.make_aware(timezone.datetime(2024, 10, 20, 12, 0, 0)),
            is_done=False,
        )
        self.task.tags.set([tag1, tag2])

    def test_task_creation(self):
        self.assertEqual(self.task.content, "Test Task")
        self.assertEqual(self.task.deadline, timezone.make_aware(timezone.datetime(2024, 10, 20, 12, 0, 0)))
        self.assertEqual(self.task.is_done, False)
        self.assertEqual(self.task.tags.count(), 2)

    def test_form_valid_data(self):
        form_data = {
            "content": "Test task content",
            "deadline": "2024-10-20 12:12"
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_deadline(self):
        form_data = {
            "content": "Test task content",
            "deadline": "invalid-date-format"
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_form_empty_data(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)