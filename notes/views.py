from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from .models import Note, Tag, Profile
from .forms import NoteForm, UserRegisterForm, SearchForm


# Главная страница - список пользователей
def home(request):
    users = User.objects.annotate(note_count=Count('note')).order_by('-note_count')
    return render(request, 'notes/home.html', {'users': users})


# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = UserRegisterForm()
    return render(request, 'notes/register.html', {'form': form})


# Вход
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('note_list')
    return render(request, 'notes/login.html')


# Выход
def user_logout(request):
    logout(request)
    return redirect('home')


# Список заметок пользователя
from django.db.models import Q


@login_required
def note_list(request):
    # Получаем заметки в зависимости от прав
    if request.user.is_staff or request.user.is_superuser:
        notes = Note.objects.all()
    else:
        notes = Note.objects.filter(user=request.user)

    # Поиск
    search_form = SearchForm(request.GET)
    search_query = ""

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('query', '').strip()

        if search_query:
            # РАЗБИВАЕМ запрос на отдельные слова
            search_words = search_query.split()

            # Начинаем с пустого Q объекта
            q_objects = Q()

            for word in search_words:
                if word:  # проверяем что слово не пустое
                    # Ищем слово в заголовке
                    q_objects |= Q(title__icontains=word)
                    # Ищем слово в тексте
                    q_objects |= Q(content__icontains=word)
                    # Ищем слово в тегах
                    q_objects |= Q(tags__name__icontains=word)

            # Применяем фильтр
            notes = notes.filter(q_objects).distinct()

    # Получаем все теги для текущего набора заметок (для облака тегов)
    all_tags = Tag.objects.filter(note__in=notes).distinct()

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'search_form': search_form,
        'search_query': search_query,
        'all_tags': all_tags,
    })

# Создание заметки
@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # привязываем к текущему пользователю
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

# Редактирование заметки
@login_required
def note_edit(request, pk):
    # Проверяем права доступа
    if request.user.is_staff or request.user.is_superuser:
        # Админ может редактировать ЛЮБУЮ заметку
        note = get_object_or_404(Note, pk=pk)
    else:
        # Обычный пользователь - только свою
        note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_form.html', {'form': form})

# Просмотр заметки
@login_required
def note_detail(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        note = get_object_or_404(Note, pk=pk)  # ← ЛЮБАЯ заметка
    else:
        note = get_object_or_404(Note, pk=pk, user=request.user)  # ← только своя

    return render(request, 'notes/note_detail.html', {'note': note})

# Удаление заметки
@login_required
def note_delete(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        # Админ может удалить ЛЮБУЮ заметку
        note = get_object_or_404(Note, pk=pk)
    else:
        # Обычный пользователь - только свою
        note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('note_list')

    return render(request, 'notes/note_confirm_delete.html', {'note': note})


