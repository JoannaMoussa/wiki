from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("wiki/<str:title>/save", views.save_changes, name="save_changes"),
    path("search", views.search, name="search"),
    path("newPage", views.new_page, name="new_page"),
    path("newPage/submit", views.submit_newpage, name="submit_newpage"),
    path("randomPage", views.random_page, name="random_page"),
    path("deletePage/<str:title>", views.delete_page, name="delete_page")
]
