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

    def fill_authors(self, cnt):
        # objs = list()
        users = list()
        for i in range(cnt):
            users.append(models.UserProfile(username=f.name()))
            print(i)
            if i % 1000 == 0 and i != 0:
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
            if i % 1000 == 0 and i != 0:
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
            if i % 1000 == 0 and i != 0:
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
            if i % 1000 == 0 and i != 0:
                models.Answer.objects.bulk_create(objs=objs)
                objs.clear()
                counter = 0
        models.Answer.objects.bulk_create(objs=objs)

    def handle(self, *args, **options):
        self.fill_authors(options.get('authors', 15))
        self.fill_tags(options.get('tags', 15))
        self.fill_questions(options.get('questions', 15))
        self.fill_answers(options.get('answers', 15))