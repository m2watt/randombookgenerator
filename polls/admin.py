from django.contrib import admin

# Register your models here.
from .models import Question, Choice, User, Library, Book


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


class LibraryInLine(admin.TabularInline):
    model = Library


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'password']
    inlines = [LibraryInLine]


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)



