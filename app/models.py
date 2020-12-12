from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum

class ProfileManager(models.Manager):
	def get_all_users(self):
 		return self.all()

	def get_best_users(self):
 		return self.all()[:15]

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='static/img/', default = 'static/img/profile.png', null=True, blank=True, verbose_name='Ава')
    email = models.EmailField(verbose_name = 'E-mail', default = 'default@def.com', blank = True)

    class Meta:
        verbose_name = 'Профиль'

    def __str__(self):
        return self.username


class TagManager(models.Manager):
    def best_tags(self):
        return self.order_by('-count')[0:3]


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка", unique="True")

    count = models.IntegerField(verbose_name="Число упоминаний", default=0)

    objects = TagManager()

    def __str__(self):
        return self.title


class QuestionManager(models.Manager):
    def best_published(self):
        return self.order_by('-like')

    def new_published(self):
        return self.order_by('-create_date')

    def by_tag(self, tag):
        return self.filter(is_active=True, tags__title=tag)


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса", unique="True")
    text = models.TextField(verbose_name=u"Полное описание вопроса")

    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")

    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    tags = models.ManyToManyField(Tag, blank=True)
    objects = QuestionManager()

    like = GenericRelation(LikeDislike, related_query_name='Question')
    unique_together = [['like', 'user']]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']

class AnswerManager(models.Manager):
    def best_answered(self):
        return self.order_by('-like')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    like = GenericRelation(LikeDislike, related_query_name='Answer')

    text = models.TextField(verbose_name='Текст ответа')
    create_date = models.DateTimeField(verbose_name='Дата ответа', default=datetime.now)

    is_correct = models.BooleanField(default=False)
    objects = AnswerManager()
    unique_together = [['like', 'user']]

    def __str__(self):
        return f'Answer text={self.text}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'