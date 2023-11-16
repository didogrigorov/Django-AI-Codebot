from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import CustomLoginView, SignUpView, DeleteCodeView, PastCodeView, HomeView, SuggestCodeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('code-suggest/', SuggestCodeView.as_view(), name="code_suggest"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(template_name = 'home.html'), name="logout"),
    path('register', SignUpView.as_view(), name="register"),
    path('past-code', PastCodeView.as_view(), name="past_code"),
    path('delete-snippet/<int:pk>', DeleteCodeView.as_view(), name="delete_snippet"),
]