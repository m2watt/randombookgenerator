import html
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
# -*- coding: utf-8 -*-
from .forms import RegistrationForm, Loginform
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.views.generic import ListView
from .models import Question, Choice, Book, Search, Genre, User, UserManager, Library


def index(request, genre):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    search_q = Search()
    genre1 = Genre(genre)
    context = {
        'latest_question_list': latest_question_list,
        'letter': search_q.search_letter,
        'rand_num': search_q.random_number,
        'genre': genre1.genre,
        'user': request.user,

    }
    return render(request, 'polls/index.html', context)


def search_results(request, search):
    context = {
        'search': search,
        'user': request.user,
    }
    if request.method == 'GET':
        context['search2'] = request.GET['query1']
    return render(request, 'polls/search_results.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def home(request):
    context = {
        'first_user': request.user,
    }
    return render(request, 'polls/home.html', context)


def loginpage(request):
    uservalue = ''
    passwordvalue = ''

    form = Loginform(request.POST or None)
    if form.is_valid():
        uservalue = form.cleaned_data.get("email")
        passwordvalue = form.cleaned_data.get("password")

        user = authenticate(email=uservalue, password=passwordvalue)
        if user is not None:
            login(request, user, backend=None)
            context = {'form': form,
                      'error': 'The login has been successful'}
            messages.info(request, f"You are now logged in as {uservalue}.")
            return render(request, 'polls/home.html', context)
        else:
            context = {'form': form,
                      'error': 'The username and password combination is incorrect'}
            messages.error(request,"Invalid username or password.")
            return render(request, 'polls/login.html', context)

    else:
        context = {'form': form}
        return render(request, 'polls/login.html', context)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            emailvalue = form.cleaned_data.get("email")
            passwordvalue = form.cleaned_data.get("password")
            user = authenticate(email=emailvalue, password=passwordvalue)
            login(request, user, backend=None)
            context = {
                'user': user,
            }
            return render(request, 'polls/home.html', context)
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html',{'form':form})


def user_logout(request):
    logout(request)
    return render(request, 'polls/home.html')


@method_decorator(login_required, name='dispatch')
class AddBook(ListView):
    model = Library
    template_name = "polls/search_results.html"

    def post(self, request, book_name: str):
        lib_curr = Library.objects.get_or_create(user_ref_id=request.user.id)[0]
        lib_curr.save()
        try:
            lib_curr.books.get(book_isbn=book_name)
            return HttpResponse("This book is already in your library")
        except Book.DoesNotExist:
            book_curr = Book(book_isbn=book_name, book_thumbnail=request.POST.get('thumbnail', None))
            lib_curr.add_book(book_curr)
            return HttpResponse("success")


@method_decorator(login_required, name='dispatch')
class DeleteBook(ListView):
    model = Library
    template_name = "polls/my_library.html"

    def post(self, request, book_name: str):
        Book.objects.filter(book_isbn=book_name).first().delete()
        lib_curr = Library.objects.get_or_create(user_ref_id=request.user.id)[0]
        lib_final = []
        for book in lib_curr.books.all():
            lib_final.append(book)
        context = {
            'library': lib_final,
        }
        return render(request, 'polls/my_library.html', context)


@method_decorator(login_required, name='dispatch')
class MyLibrary(ListView):
    model = Book
    template_name = "polls/my_library.html"

    def post(self, request):
        lib_curr = Library.objects.get_or_create(user_ref_id=request.user.id)[0]
        lib_final = []
        for book in lib_curr.books.all():
            lib_final.append(book)
        context = {
            'library': lib_final,
        }
        return render(request, 'polls/my_library.html', context)

