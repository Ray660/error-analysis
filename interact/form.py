from django import forms
from master.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic', 'type', 'photo']
