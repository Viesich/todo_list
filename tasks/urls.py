from django.urls import path
from tasks.views import TodoList, TagList

app_name = "tasks"
urlpatterns = [
    path("", TodoList.as_view(), name="index"),
    path("tags/", TagList.as_view(), name="tags"),
]
