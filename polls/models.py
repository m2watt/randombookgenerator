from django.db import models
from django.utils import timezone
from random import randint
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from typing import List

import polls.models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING,)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Book(models.Model):
    book_isbn = models.CharField(max_length=200)
    book_thumbnail = models.CharField(max_length=200)

    class Meta:
        ordering = ['book_isbn']

    def __str__(self):
        return str(self.book_isbn)


class Search(models.Model):
    search_letter: str
    random_number: int

    def __init__(self):
        super().__init__()
        randum = randint(0, 25)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        self.search_letter = letters[randum]
        self.random_number = randint(0, 39)


class Genre(models.Model):
    genre: str

    def __init__(self, genre_name):
        super().__init__()
        self.genre = genre_name


class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    # Method called while creating a staff user
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False

        return self.save_user(email, password, **extra_fields)

        # Method called while calling createsuperuser
    def create_superuser(self, email, password, **extra_fields):

        # Set is_superuser parameter to true
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')

        extra_fields['is_staff'] = True

        return self.save_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # Primary key of the model
    id = models.BigAutoField(
        primary_key = True,
        auto_created = True,
        verbose_name = "ID",
    )

    first_name = models.CharField(
        max_length = 20,
        verbose_name = "First Name",
    )

    last_name = models.CharField(
        max_length = 20,
        verbose_name = "Last Name",
    )

    # Email field that serves as the username field
    email = models.CharField(
        max_length = 50,
        unique = True,
        validators = [validators.EmailValidator()],
        verbose_name = "email"
    )


    password = models.CharField(
        max_length = 50,
        unique = False,
        verbose_name = "Password"
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    x = 5
    # Other required fields for authentication
    # If the user is a staff, defaults to false
    is_staff = models.BooleanField(default=False)

    # If the user account is active or not. Defaults to True.
    # If the value is set to false, user will not be allowed to sign in.
    is_active = models.BooleanField(default=True)

    # Setting email instead of username
    # Custom user manager
    objects = UserManager()

    def get_full_name(self):
        # Returns the first_name and the last_name
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name


class Library(models.Model):
    books: models.ManyToManyField(Book)
    user_ref: models.ForeignKey(User, default="none", related_name="user", on_delete=models.CASCADE)

    books = models.ManyToManyField(Book)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, default="id")

    def add_book(self, book: Book):
        book.save()
        self.books.add(book)

    def remove_book(self, book_isbn:str):
        for book in self.books.all():
            if book.book_isbn == book_isbn:
                self.books.remove(book)


    def get_books(self):
        return self.books







