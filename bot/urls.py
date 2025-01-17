from django.urls import path
from . import views

urlpatterns = [
    path("",views.chat,name = "chatbot"),
    path("session",views.session,name = "session")
]