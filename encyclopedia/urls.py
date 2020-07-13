from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:wiki_name>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("wiki/<str:wiki_name>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    

]
