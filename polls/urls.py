from django.conf.urls import url
import re
from . import views
from polls.views import AddBook, MyLibrary, DeleteBook


urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^index/(?P<genre>[A-Za-z ]*)/$', views.index, name='index'),
    url(r'^(?P<search>.*)/search_results$', views.search_results, name='search_results'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    # ex: /polls/5/vote/
    url(r'^login/$', views.login_request, name='login'),
    url(r'^register/$', views.register_request, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<book_name>[A-Za-z ]+)/add_book/$', AddBook.as_view(), name="add_book"),
    url(r'^my_library/$', MyLibrary.as_view(), name="my_library"),
    url(r'^(?P<book_name>[A-Za-z ]+)/delete_book/$', DeleteBook.as_view(), name="delete_book"),
]
