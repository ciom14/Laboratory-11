from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Note, Tag


# Форма для регистрации пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма для создания/редактирования заметки
class NoteForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='Теги (через запятую)',
        help_text='Введите теги через запятую'
    )

    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Если заметка уже существует
            self.fields['tags_input'].initial = self.instance.get_tags_as_string()

    def save(self, commit=True, user=None):
        note = super().save(commit=False)

        # Если это новая заметка (нет pk) и передан пользователь
        if not note.pk and user:
            note.user = user

        if commit:
            note.save()

            # Обрабатываем теги
            tags_str = self.cleaned_data.get('tags_input', '')
            if tags_str:
                # Разбиваем строку тегов, убираем пробелы, фильтруем пустые
                tag_names = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]

                # Очищаем старые теги
                note.tags.clear()

                # Добавляем новые теги
                for tag_name in tag_names:
                    # Создаем или получаем тег (приводим к нижнему регистру)
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    note.tags.add(tag)

        return note


# Форма для поиска
class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по заголовку, тексту или тегам',
            'class': 'form-control'
        }),
        max_length=100
    )

