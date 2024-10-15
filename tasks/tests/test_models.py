from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from tasks.models import Task, Tag


class ModelsTests(TestCase):

    def test_task_str(self) -> None:
        task = Task.objects.create(
            content="Test Task",
            deadline=timezone.now()
        )
        self.assertEqual(str(task), "Test Task")

    def test_default_value_is_done_task(self):
        task = Task.objects.create(
            content="Test Task",
            deadline=timezone.now()
        )
        self.assertEqual(task.is_done, False)

    def test_tag_str(self) -> None:
        tag = Tag.objects.create(
            name="Test",
            deadline=timezone.now()
        )
        self.assertEqual(str(tag), "Test")

    def test_task_tag_relationship(self):
        tag1 = Tag.objects.create(name="Test1")
        tag2 = Tag.objects.create(name="Test2")
        task = Task.objects.create(
            content="Test Task",
            deadline=timezone.now()
        )
        task.tags.set([tag1, tag2])
        self.assertIn(tag1, task.tags.all())

    def test_tag_name_length(self):
        tag = Tag.objects.create(name="T" * 51)
        with self.assertRaises(ValidationError):
            tag.full_clean()
