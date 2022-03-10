import html
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
# -*- coding: utf-8 -*-
from .forms import NewUserForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.views.generic import ListView
from .models import Question, Choice, Book, Search, Genre, User, UserManager, Library
from django.contrib.auth.hashers import make_password
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm


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
        lib_curr = Library.objects.get_or_create(user_ref_id=request.user.id)[0]
        lib_curr.remove_book(book_name)
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

    def get(self, request):
        try:
            lib_curr = Library.objects.filter(user_ref_id=request.user.id)[0]
        except:
            lib_curr = Library.objects.get_or_create(user_ref_id=request.user.id)[0]
        lib_final = []

        for book in lib_curr.books.all():
            lib_final.append(book)
        context = {
            'library': lib_final,
        }
        return render(request, 'polls/my_library.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return render(request, 'polls/home.html', context={"username":email})
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="polls/login.html", context={"login_form":form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return render(request, 'polls/home.html', context={"username":""})
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})
