from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from app import models
from app.forms import *
from math import ceil


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

def logout(request):
    auth.logout(request)
    redirect_path = request.GET.get('next', '/')
    return redirect(redirect_path)

def login(request):
    redirect_to = request.GET.get('next', '/')
    error_message = None
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(redirect_to)
            else:
                error_message = "Incorrect login or password"

    ctx = { 
        'form': form, 
        'redirect_to': redirect_to, 
        'error_message': error_message 
        }
    return render(request, 'login.html', ctx)

def register(request):
    if request.method == 'GET':
        form_profile = CreateProfileForm()
        form_user = CreateUserForm()
    else:
        data = request.POST
        profileData = { 'avatar': data.get('avatar') }
        userData = { 'username': data.get('username'), 'email': data.get('email'), 'password': data.get('password') }
        formProfile = CreateProfileForm(data = profileData)
        formUser = CreateUserForm(data = userData)
        if formProfile.is_valid() and formUser.is_valid():
            data = formUser.cleaned_data
            user = User.objects.create_user(username = data.get('username'), email = data.get('email'), password = data.get('password'))
            profile = formProfile.save(commit = False)
            profile.user = user
            profile.user_name = data.get('username')
            profile.email = data.get('email')
            profile.save()
            auth.login(request, user)
            return redirect("/")
    ctx = { 'form_profile': formProfile, 'form_user': formUser }
    return render(request, 'signup.html', ctx)

@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.save()
            question.tags.set(form.cleaned_data['tags'])
            return redirect(reverse('question', kwargs = {'pk': question.pk}))

    ctx = { 
        'form': form 
        }
    return render(request, 'ask.html', ctx)

def questionPage(request, pk):
    question = models.Question.objects.get(pk=pk)
    answers = question.answer_set.all()
    answersPage, page = paginate(answers, request)

    OBJECTS_PER_PAGE = 3
    paginator = Paginator(answers, OBJECTS_PER_PAGE)

    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data = request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            if request.user.is_authenticated:
                answer.author = request.user
                answer.question = Question.objects.get(pk = pk)
                answer.save()

                if paginator.count % OBJECTS_PER_PAGE == 0:
                    pageNumberForRef = paginator.num_pages + 1
                else:
                    pageNumberForRef = paginator.num_pages
                return redirect(reverse('question', kwargs = {'pk': question.pk}) + f'?page={ pageNumberForRef }#{ answer.id }')
            else:
                path = reverse('login') + f'?next=/question/{ pk }&anchor=scroll-to-form'
                return redirect(path)
    ctx = {'question': question, 'answers': answersPage, 'page': page, 'form': form}
    return render(request, 'question_page.html', ctx)

def tagSearch(request, pk):
    questions_ = models.Question.objects.by_tag(pk)
    questionsPage, page = paginate(questions_, request)
    return render(request, 'questions_tag.html', {
        'page': page,
        'questions': questionsPage,
        'tag': pk,
    })

@login_required
def settings(request):
    cur_user = request.user
    if request.method == 'GET':
        form = EditProfileForm(data = { 'username': cur_user.username, 'email': cur_user.email})
    else:
        form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            cur_user.username = data.get('username')
            cur_user.email = data.get('email')
            cur_user.avatar = data.get('avatar')
            request.user.username = data.get('username')
            request.user.email = data.get('email')
            cur_user.save()
            request.user.save()

    ctx = { 'form': form }
    return render(request, 'settings.html', ctx)