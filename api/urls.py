from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name="routes"),
    path("register/", views.register, name="register"),
    path("entries/", views.getDiaryEntries, name="entries"),
    path("entries/<str:pk>", views.getDiaryEntry, name="entry"),
    path("entries/create", views.createDiaryEntry, name="create-diary"),
    path("entries/<str:pk>/update", views.updateDiaryEntry),
    path("entries/<str:pk>/delete", views.deleteDiaryEntry, name="delete-diary"),
]
