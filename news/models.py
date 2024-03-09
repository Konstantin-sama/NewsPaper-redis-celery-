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
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authors')
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
    subscribers = models.ManyToManyField(User, max_length=64, blank=True, related_name='categories')
    # subscribers = models.ManyToManyField(User, null=True, blank=True, related_name='categories')
    # связь многие ко многим с моделью пользователь

    def __str__(self):
        return f'{self.name}'
        # return self.name


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
        return f'{self.categoryType.CATEGORY_CHOICES}'
        # выбор категории


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
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
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
#
# 1 quest Создаем пользователей:
# u1 = User.objects.create_user(username='Иванов Иван Иванович')
# u1
# u2 = User.objects.create_user(username='Петров Петр Петрович')
# u2
# u3 = User.objects.create_user(username='Максимов Максим Максимович')
# u3
# u4 = User.objects.create_user(username='Калинкин Константин Владимирович')
#
# Создаем авторов:
# Author.objects.create(authorUser=u1)
# result: <Author: Author object (1)>
# Author.objects.create(authorUser=u2)
# result: <Author: Author object (2)>
#
# Создаем категории:
#   >>> Category.objects.create(name='IT')
# 	<Category: Category object (1)>
# 	>>> Category.objects.create(name='Sport')
# 	<Category: Category object (2)>
# 	>>> Category.objects.create(name='Politics')
# 	<Category: Category object (3)>
# 	>>> Category.objects.create(name='Education')
# 	<Category: Category object (4)>
# 	>>> Category.objects.create(name='Finance')
# 	<Category: Category object (5)>
#
# Получаем автора по id:
#   >>> author = Author.objects.get(id=1)
# 	>>> author
# 	<Author: Author object (1)>
# 	>>> author2 = Author.objects.get(id=2)
# 	>>> author2
# 	<Author: Author object (2)>
#
# Создаем пост:
#   >>> Post.objects.create(author=author, categoryType='NW', title='Восстание человека', text='Как обойти ИИ и стать умнее? На этот вопрос ответит издательство от SkillFactory!')
# 	<Post: Post object (1)>
# 	>>> Post.objects.get(id=1).title # Post.objects.get(id=1).text
# 	'Восстание человека'
# 	>>> Post.objects.create(author=author, categoryType='AR', title='Workout', text='Make sport is very healthy')
# 	<Post: Post object (2)>
# 	>>> Post.objects.create(author=author2, categoryType='AR', title='Python', text='Hello world!')
# 	<Post: Post object (3)>
#
# К статьям/новостям присваиваем категории:
#
#   >>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=1))
# 	>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=2))
# 	>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=1))
# 	>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=3))
# 	>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=4))
# 	>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=3))
#
# Создаем комментарии к статьям/новостям:
# 	>>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=1).authorUser, text='Greate post')
# 	<Comment: Comment object (1)>
# 	>>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=2).authorUser, text='Interesting news')
# 	<Comment: Comment object (2)>
# 	>>> Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=2).authorUser, text='Get over yourself')
# 	<Comment: Comment object (3)>
# 	>>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=1).authorUser, text='Python is the best computer program')
# 	<Comment: Comment object (4)>
# 	>>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=2).authorUser, text='Hello Skillfactory')
# 	<Comment: Comment object (5)>
#
# Применяем функции like() и dislike() к комментариям:
#
#   >>> Comment.objects.get(id=1).like()
# 	>>> Comment.objects.get(id=1).rating
# 	1
# 	>>> Comment.objects.get(id=1).dislike()
# 	>>> Comment.objects.get(id=1).dislike()
# 	>>> Comment.objects.get(id=1).dislike()
# 	>>> Comment.objects.get(id=1).rating
# 	-2
# 	>>> Comment.objects.get(id=2).like()
# 	>>> Comment.objects.get(id=2).like()
# 	>>> Comment.objects.get(id=2).like()
# 	>>> Comment.objects.get(id=3).like()
# 	>>> Comment.objects.get(id=3).like()
# 	>>> Comment.objects.get(id=4).like()
# 	>>> Comment.objects.get(id=5).dislike()
#
# Применяем функции like() и dislike() к статьям/новостям:
#   >>> Post.objects.get(id=1).like()
# 	>>> Post.objects.get(id=1).rating
# 	1
# 	>>> Post.objects.get(id=1).like()
# 	>>> Post.objects.get(id=1).like()
# 	>>> Post.objects.get(id=1).like()
# 	>>> Post.objects.get(id=1).like()
# 	>>> Post.objects.get(id=1).like()
# 	>>> Post.objects.get(id=2).like()
# 	>>> Post.objects.get(id=2).like()
# 	>>> Post.objects.get(id=2).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).like()
# 	>>> Post.objects.get(id=3).dislike()
# 	>>> Post.objects.get(id=1).dislike()
# 	>>> Post.objects.get(id=1).dislike()
#
# Создал комментарии для User id 3 и 4:
#   >>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=User.objects.get(id=3), text='Hello Skillfactory')
# 	<Comment: Comment object (6)>
# 	>>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=User.objects.get(id=4), text='An interesting question')
# 	<Comment: Comment object (7)>
#
# Применяем функции like() и dislike() к этим комментариям:
# 	>>> Comment.objects.get(id=6).like()
# 	>>> Comment.objects.get(id=7).like()
#
# Получаем автора по id:
# 	>>> Author.objects.get(id=1)
# 	<Author: Author object (1)>
#
# Присваиваем в переменную а и b и обновляем рейтинги пользователей:
# 	>>> a = Author.objects.get(id=1)
# 	>>> a.update_rating()
# 	>>> a.ratingAuthor
# 	18
# 	>>> b = Author.objects.get(id=2)
# 	>>> b.update_rating()
# 	>>> b.ratingAuthor
# 	26
#
# Выводим рейтинг лучшего пользователя применяя сортировку:
# 	>>> a = Author.objects.order_by('-ratingAuthor')[:1]
# 	>>> a
# 	<QuerySet [<Author: Author object (2)>]>
#
# Выводим рейтинги всех пользователей применяя сортировку:
# 	>>> a = Author.objects.order_by('-ratingAuthor')
# 	>>> a
# 	<QuerySet [<Author: Author object (2)>, <Author: Author object (1)>]>
#
# Выводим рейтинги и всех пользователей применяя цикл for:
# 	>>> for i in a:
# 	...     i.ratingAuthor
# 	...     i.authorUser.username
# 	...
# 	25
# 	'Петров Петр Петрович'
# 	20
# 	'Иванов Иван Иванович'
#
# Применяем метод preview() к постам:
# 	>>> Post.objects.get(id=1).preview()
# 	'Как обойти ИИ и стать умнее?...'
# 	>>> Post.objects.get(id=3).preview()
# 	'Hello world!...'
#
# Определяем лучшей пост по лайкам и диз-лайкам:
# 	>>> bestPost = Post.objects.order_by('-rating')[:1]
# 	>>> bestPost
# 	<QuerySet [<Post: Post object (3)>]>
#
# Выводим дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
# 	>>> for i in bestPost:
# 	...     i.dateCreation
# 	...     i.author.authorUser
# 	...     i.rating
# 	...     i.title
# 	...     i.preview()
# 	...
#
# Выводим все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
# 	>>> bestPostCom = Comment.objects.filter(commentPost=3)
# 	>>> bestPostCom
# 	<QuerySet [<Comment: Comment object (4)>, <Comment: Comment object (5)>, <Comment: Comment object (6)>]>
# 	>>>
#
# Выводим через цикл for:
# 	>>> for k in bestPostCom:
# 	...     k.dateCreating
# 	...     k.commentUser
# 	...     k.rating
# 	...     k.text
# 	...
# 	datetime.datetime(2021, 12, 17, 17, 27, 46, 361544, tzinfo=datetime.timezone.utc)
# 	<User: Иванов Иван Иванович>
# 	1
# 	'Python is the best computer program'
# 	datetime.datetime(2021, 12, 17, 17, 30, 8, 679615, tzinfo=datetime.timezone.utc)
# 	<User: Петров Петр Петрович>
# 	-1
# 	'Hello Skillfactory'
# 	datetime.datetime(2021, 12, 17, 17, 49, 23, 418566, tzinfo=datetime.timezone.utc)
# 	<User: Максимов Максим Максимович>
# 	1
# 	'Hello Skillfactory'
# 	>>>
#
# 2-ой вариант через values:
# 	>>> bestPostCom.values("dateCreating", "commentUser", "rating", "text")
#
# 	<QuerySet [{'dateCreating': datetime.datetime(2021, 12, 17, 17, 27, 46, 361544,
# 	tzinfo=datetime.timezone.utc), 'commentUser': 1, 'rating': 1, 'text': 'Python is the best
# 	computer program'}, {'dateCreating': datetime.datetime(2021, 12, 17, 17, 30, 8, 679615, tzinfo
# 	=datetime.timezone.utc), 'commentUser': 2, 'rating': -1, 'text': 'Hello Skillfactory
# 	'}, {'dateCreating': datetime.datetime(2021, 12, 17, 17, 49, 23, 418566, tzinfo=date
# 	time.timezone.utc), 'commentUser': 3, 'rating': 1, 'text': 'Hello Skillfactory'}]>
# 	>>>