from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app import models
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--likes', type=int)

    def fill_authors(self, cnt):
        # objs = list()
        users = list()
        for i in range(cnt):
            users.append(models.UserProfile(username=f.name()))
            print(i)
            if i % 1e7 == 0 and i != 0:
                models.UserProfile.objects.bulk_create(objs=users)
                users.clear()
        models.UserProfile.objects.bulk_create(objs=users)

    def fill_tags(self, cnt):
        objs = list()
        for i in range(cnt):
            objs.append(models.Tag(
                title=f.sentence()[:128],
                count=f.random_int(min=0, max=10)
            ))
            if i % 1e7 == 0 and i != 0:
                models.Tag.objects.bulk_create(objs=objs)
                objs.clear()
        models.Tag.objects.bulk_create(objs=objs)

    def fill_questions(self, cnt):
        objs = list()
        authors_ids = list(models.UserProfile.objects.values_list('id', flat=True))
        for i in range(cnt):
            objs.append(models.Question(
                author_id=choice(authors_ids),
                title=f.sentence()[:28],
                text=f.sentence()[:46],
            ))
            if i % 1e7 == 0 and i != 0:
                models.Question.objects.bulk_create(objs=objs)
                objs.clear()

        models.Question.objects.bulk_create(objs=objs)
        objects = models.Question.objects.all()
        tags_ids = models.Tag.objects.values_list('id', flat=True)
        for i in range(cnt):
            objects[i].tags.add(choice(tags_ids))
        models.Question.objects.update()

    def fill_answers(self, cnt):
        objs = list()
        authors_ids = models.UserProfile.objects.values_list('id', flat=True)
        questions_ids = models.Question.objects.values_list('id', flat=True)
        counter = 0
        for i in range(cnt):
            objs.append(models.Answer(
                text=f.sentence()[:46],
                author_id=choice(authors_ids)
            ))
            id = choice(questions_ids)
            objs[counter].question = models.Question.objects.get(pk=id)
            counter += 1
            if i % 1e7 == 0 and i != 0:
                models.Answer.objects.bulk_create(objs=objs)
                objs.clear()
                counter = 0
        models.Answer.objects.bulk_create(objs=objs)

    def get_random_user_id(self):
        user_id = list(
            models.UserProfile.objects.values_list(
                'id', flat=True
            )
        )
        return choice(user_id)

    def get_random_question_id(self):
        questions_id = list(
            models.Question.objects.values_list(
                'id', flat=True
            )
        )
        return choice(questions_id)

    def get_random_answer_id(self):
        answer_id = list(
            models.Answer.objects.values_list(
                'id', flat=True
            )
        )
        return choice(answer_id)

    def fill_likes(self, cnt):
        for i in range(cnt):
            like_answer = models.LikeAnswer()
            like_question = models.LikeQuestion()

            qst = models.Question.objects.get(id = self.get_random_question_id())
            like_question.question_id = qst.id

            like_answer.answer_id = self.get_random_answer_id()

            if (f.random_int(min=1, max=10) < 4):
                like_answer.is_like = False
                like_question.is_like = False
            else:
                like_answer.is_like = True
                like_question.is_like = True

            like_question.user_id = self.get_random_user_id()
            like_answer.user_id = self.get_random_user_id()

            try:
                like_answer.save()
                like_question.save()
                qst.save()

            except IntegrityError:
                continue

    def handle(self, *args, **options):
        self.fill_authors(options.get('authors', 15))
        self.fill_tags(options.get('tags', 15))
        self.fill_questions(options.get('questions', 15))
        self.fill_answers(options.get('answers', 15))
        self.fill_likes(options.get('likes', 15))