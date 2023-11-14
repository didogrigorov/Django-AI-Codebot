from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import CustomLoginView, SignUpView, DeleteCodeView

urlpatterns = [
    path('', views.home, name="home"),
    path('code-suggest/', views.code_suggest, name="code_suggest"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(template_name = 'home.html'), name="logout"),
    path('register', SignUpView.as_view(), name="register"),
    path('past-code', views.past_code, name="past_code"),
    path('delete-snippet/<int:pk>', DeleteCodeView.as_view(), name="delete_snippet"),
]