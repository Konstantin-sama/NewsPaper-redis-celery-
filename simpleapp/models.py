from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator

# импорт базы данных
# импорт django-регистрации
# импорт метода сумма
# коллекцию вызываемых validators для использования с полями модели и формы (лайк и дизлайк)


class Author(models.Model):
    # модель автор
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    # регистрация пользователя
    ratingAuthor = models.SmallIntegerField(default=0)
    # рейтинг пользователя (автор)

    def update_rating(self):
        # функция обновление рейтинга
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        # рейтинг публикации
        pRat = 0
        # счетчик по умолчанию
        pRat += postRat.get('postRating')
        # обновление рейтинга
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        # рейтинг комментария
        cRat = 0
        # счетчик по умолчанию
        cRat += commentRat.get('commentRating')
        # обновление рейтинга

        self.ratingAuthor = pRat * 3 + cRat
        self.save()
        # суммарный рейтинг статьи автора умножается на 3

    def __str__(self):
        # method принимает в качестве аргумента только self
        return f'{self.authorUser.username}'
        # выводит имя пользователя (автора)


class Category(models.Model):
    # модель категория
    name = models.CharField(max_length=64, unique=True)
    # поле название с ограничениями (длина=64, уникальное)
    subscribers = models.ManyToManyField(User, max_length=64, blank=True)
    # (null=True)
    # связь многие ко многим с моделью пользователь

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    # модель публикация
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # поле автор+ связь один ко многим

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    # переменные новости, статья, выбор категории,

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    # поле выбор категории
    dateCreation = models.DateTimeField(auto_now_add=True)
    # дата публикации
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    # поле категории публикации
    title = models.CharField(max_length=128)
    # заголовок
    text = models.TextField()
    # текст
    rating = models.SmallIntegerField(default=0)
    # рейтинг публикации

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
        # метод лайк и дизлайк

    def preview(self):
        return self.text[0:123] + '...'
        # метод preview() модели Post, который возвращает начало статьи

    def get_absolute_url(self):
        return f'/news/{self.id}'
        # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром

    def __str__(self):
        return self.get_categoryType_display()


class PostCategory(models.Model):
    # промежуточная модель категория публикации (связь один ко многим)
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    # поле публикации (связь один ко многим)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    # поле категории (связь один ко многим)


class Comment(models.Model):
    # модель комментарий
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    # комментарий публикации
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    # комментарий пользователя
    text = models.TextField()
    # текст комментария
    dateCreating = models.DateTimeField(auto_now_add=True)
    # дата добавления комментария
    rating = models.SmallIntegerField(default=0)
    # рейтинг комментария

    def like(self):
        self.rating += 1
        self.save()
        # лайк комментария

    def dislike(self):
        self.rating -= 1
        self.save()
        # дизлайк комментария

# python manage.py shell
# from news.models import *

# К статьям/новостям присваиваем категории:
#
#   >>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=1))
# 	>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=2))
# 	>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=1))
# 	>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=3))
# 	>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=4))
# 	>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=3))