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
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/',
                                default = 'profile.png',
                                blank = True,
                                verbose_name='Аватарка')
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
        return self.order_by('-likequestion', '-create_date')

    def new_published(self):
        return self.order_by('-create_date')

    def by_tag(self, tag):
        return self.filter(is_active=True, tags__title=tag)

    def question_by_pk(self, pk):
        return self.get(pk = pk)


class LikeManager(models.Manager):
    def likes_user(self, user):
        self.filter(user = user)



class LikeQuestion(models.Model):
    is_like = models.BooleanField(verbose_name='Лайк? (или дизлайк)')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    objects = LikeManager()

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together = ['question', 'user']


class LikeAnswer(models.Model):
    is_like = models.BooleanField(verbose_name='Лайк? (или дизлайк)')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together = ['answer', 'user']


class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса", unique="True")
    text = models.TextField(verbose_name=u"Полное описание вопроса")

    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    rating = models.IntegerField(default = 0, blank = True, verbose_name = 'Рейтинг')
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    tags = models.ManyToManyField(Tag, blank=True)
    objects = QuestionManager()

    like = GenericRelation(LikeQuestion, related_query_name='Question')
    unique_together = [['like', 'user']]

    def answer(self):
        return Answer.objects.filter(question = self).count()
        
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']

    def like(self):
        like = LikeQuestion.objects.filter(question = self, is_like = True).count()
        print('like', like)
        dislike = LikeQuestion.objects.filter(question = self, is_like = False).count()
        return like - dislike

    def answer(self):
        return Answer.objects.filter(question = self).count()

class AnswerManager(models.Manager):
    def best_answered(self):
        return self.order_by('-like')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    like = GenericRelation(LikeAnswer, related_query_name='Answer')

    text = models.TextField(verbose_name='Текст ответа')
    create_date = models.DateTimeField(verbose_name='Дата ответа', default=datetime.now)

    is_correct = models.BooleanField(default=False)
    objects = AnswerManager()
    unique_together = [['like', 'user']]

    def like(self):
        like = LikeAnswer.objects.filter(answer = self, is_like = True).count()
        dislike = LikeAnswer.objects.filter(answer = self, is_like = False).count()
        return like - dislike

    def __str__(self):
        return f'Answer text={self.text}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'