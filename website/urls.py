from django.urls import path

from . import views
from .views import (
    CustomLoginView,
    SignUpView,
    DeleteCodeView,
    PastCodeView,
    HomeView,
    SuggestCodeView
)

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('code-suggest/', SuggestCodeView.as_view(), name="code_suggest"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(template_name = 'home.html'), name="logout"),
    path('register', SignUpView.as_view(), name="register"),
    path('past-code', PastCodeView.as_view(), name="past_code"),
    path('delete-snippet/<int:pk>', DeleteCodeView.as_view(), name="delete_snippet"),
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html', html_email_template_name='password_reset_email.html'), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]