from django.urls import path
from tasks.views import (
    TaskList,
    TagList,
    TagCreate,
    TagUpdate,
    TagDelete,
    TaskCreate,
    TaskAddTag,
    TaskRemoveTag,
    change_status,
)

app_name = "tasks"
urlpatterns = [
    path("", TaskList.as_view(), name="index"),
    path("task/<int:pk>/add_tags/", TaskAddTag.as_view(), name="task-add-tag"),
    path(
        "task/<int:pk>/remove_tags/",
        TaskRemoveTag.as_view(),
        name="task-remove-tag"
    ),
    path(
        "task/<int:pk>/toggle_done/", change_status, name="task_change-status"
    ),
    path("tags/", TagList.as_view(), name="tags"),
    path("tags/create/", TagCreate.as_view(), name="tag_create"),
    path("tags/<int:pk>/", TagUpdate.as_view(), name="tag_update"),
    path("tags/<int:pk>/delete/", TagDelete.as_view(), name="tag_delete"),
    path("task/create/", TaskCreate.as_view(), name="task_create"),
]
