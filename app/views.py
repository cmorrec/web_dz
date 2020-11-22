from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from math import ceil
from app import models

# Create your views here.

def right_block(request):
    return {'bestMembers': bestMembers,
            'popularTags': popularTags,}

def is_login(request):
    return {'userName': userName,
        'isLogin': isLogin,}



bestMembers = ['vrhaena', 'Best user after vrhaena', 'Queen of number 2', 'cmorrec', 'oki docki']
userName = 'cmorrec'
isLogin = True
popularTags = ["perl", "python", "technoPark", "Mysql", "django", "Mail.ru", "voloshin", "firefox"]



def paginate(objects_list, request, per_page=3):
    page_number = request.GET.get('page')
    if (page_number == None):
        page_number = 1

    paginator = Paginator(objects_list, per_page)
    if (paginator.num_pages == 0):
        return None, None
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page.object_list, page

def index(request):
    questions_ = models.Question.objects.all()
    questionsPage, page = paginate(questions_, request)
    return render(request, 'index.html', {
        'page': page,
        'questions': questionsPage,
    })

def indexHot(request):
    questions_ = models.Question.objects.best_published()
    questionsPage, page = paginate(questions_, request)
    return render(request, 'index_hot.html', {
        'page': page,
        'questions': questionsPage,
    })

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'signup.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def ask(request):
    return render(request, 'ask.html', {})

def questionPage(request, pk):
    question = models.Question.objects.get(pk=pk)
    answers = question.answer_set.all()
    answersPage, page = paginate(answers, request)
    return render(request, 'question_page.html', {
        'question': question,
        'answers': answersPage,
        'page': page,
    })

def tagSearch(request, pk):
    questions_ = models.Question.objects.by_tag(pk)
    questionsPage, page = paginate(questions_, request)
    return render(request, 'questions_tag.html', {
        'page': page,
        'questions': questionsPage,
        'tag': pk,
    })
