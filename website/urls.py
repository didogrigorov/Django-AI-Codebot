from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('code-suggest/', views.code_suggest, name="code_suggest"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('past-code', views.past_code, name="past_code"),
    path('delete-snippet/<int:id>', views.delete_snippet, name="delete_snippet"),
]