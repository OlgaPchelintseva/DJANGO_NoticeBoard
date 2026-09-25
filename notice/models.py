from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Информация')
    # author_name = models.CharField(max_length=50, verbose_name='Имя автора')
    author_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='notices', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        return user == self.author_name

    def can_delete(self, user):
            if not user.is_authenticated:
                return False
            return user == self.author_name

    class Meta: 
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']