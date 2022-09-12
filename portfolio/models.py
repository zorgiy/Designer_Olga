from django.contrib.auth.models import User
from django.db import models


class Design(models.Model):
    Design_title = models.CharField('Название объекта', max_length=255)
    square = models.DecimalField('Площадь м2', max_digits=5, decimal_places=0)
    author_name = models.CharField('Автор', max_length=255, default='Olga')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_designs')
    vieweds = models.ManyToManyField(User, through='UserDesignRelation', related_name='designs')

    def __str__(self):
        return f'Id {self.id}: {self.Design_title}'

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class UserDesignRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Пойдет'),
        (2, 'Хорошо'),
        (3, 'Отлично'),
        (4, 'Удивительно'),
        (5, 'Невероятно')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.design.Design_title} : {self.rate} балла'

    class Meta:
        verbose_name = 'Рейтинг пользователя'
        verbose_name_plural = 'Рейтинг пользователей'
