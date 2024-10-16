from django import forms
from tasks.models import Task, Tag


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("content", "deadline")
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class AddTagForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), label="Add a Tag")


class RemoveTagForm(forms.Form):
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        label="Remove a Tag"
    )
