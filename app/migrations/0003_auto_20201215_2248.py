# Generated by Django 3.1.3 on 2020-12-15 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201215_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(verbose_name='Лайк? (или дизлайк)')),
                ('data_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Лайк ответа',
                'verbose_name_plural': 'Лайки ответов',
                'unique_together': {('answer', 'user')},
            },
        ),
        migrations.CreateModel(
            name='LikeQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(verbose_name='Лайк? (или дизлайк)')),
                ('data_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Лайк вопроса',
                'verbose_name_plural': 'Лайки вопросов',
                'unique_together': {('question', 'user')},
            },
        ),
        migrations.DeleteModel(
            name='LikeDislike',
        ),
    ]