from django.urls import path
from tasks.views import TodoList, TagList, TagCreate, TagUpdate, TagDelete

app_name = "tasks"
urlpatterns = [
    path("", TodoList.as_view(), name="index"),
    path("tags/", TagList.as_view(), name="tags"),
    path("tags/create/", TagCreate.as_view(), name="tag_create"),
    path("tags/<int:pk>/", TagUpdate.as_view(), name="tag_update"),
    path("tags/<int:pk>/delete/", TagDelete.as_view(), name="tag_delete"),
]
