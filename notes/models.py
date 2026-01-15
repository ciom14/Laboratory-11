from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Модель профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Стандартный User уже имеет: username, email, password, first_name, last_name

    def __str__(self):
        return f'{self.user.username}'

    def get_note_count(self):
        return self.user.note_set.count()


# Сигналы для автоматического создания профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Модель тега
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Модель заметки
class Note(models.Model):
    # Связываем заметку с пользователем (автором)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Основные поля
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст заметки")

    # Даты (автоматически заполняются)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    # Теги (связь многие-ко-многим)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    # Методы
    def __str__(self):
        return self.title

    def get_tags_as_string(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    class Meta:
        ordering = ['-updated_at']  # Сортировка по умолчанию