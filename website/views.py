import os
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import render, redirect
import openai
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView

from .forms import SignUpForm
from .models import Code


# Create your views here.
def home(request):
    languages = ['C', 'Clike', 'CoffeeScript', 'cpp', 'Csharp', 'CSS', 'Dart', 'Django', 'Go', 'HTML', 'Java',
                 'Javascript', 'JSX', 'Markdown', 'Markup', 'Markup-templating', 'Matlab', 'Mongodb', 'Objective-C',
                 'Perl', 'PHP', 'Powershell', 'Python', 'R', 'Ruby', 'Rust', 'Sass', 'Scala', 'Scss', 'SQL', 'Swift',
                 'TSX', 'Typescript']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        # Check if lang is empty
        if lang == "Select Programming Language":
            messages.success(request, "Hey! You Forgot to Pick a Programming Language!")
            return render(request, 'home.html', {"lang_list": languages, "code": code, "lang": lang})
        else:
            # OpenAI Key
            openai.api_key = os.getenv('OPENAI_API_KEY')
            # OpenAI Instance
            openai.Model.list()

            try:
                response = openai.Completion.create(
                    model='gpt-3.5-turbo-instruct',
                    prompt=f"Respond only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0

                )
                # Response Parsing
                response = (response['choices'][0]['text']).strip()
                # Save a snippet to the database
                record = Code(question=code, code_response=response, language=lang, user=request.user)
                record.save()
                return render(request, 'home.html', {"lang_list": languages, "response": response, "lang": lang})

            except Exception as e:
                return render(request, 'home.html', {"lang_list": languages, "code": e, "lang": lang})

        # return render(request, 'home.html', {"lang_list": languages, "code": code, "lang": lang})

    return render(request, 'home.html', {"lang_list": languages})


def code_suggest(request):
    languages = ['C', 'Clike', 'CoffeeScript', 'cpp', 'Csharp', 'CSS', 'Dart', 'Django', 'Go', 'HTML', 'Java',
                 'Javascript', 'JSX', 'Markdown', 'Markup', 'Markup-templating', 'Matlab', 'Mongodb', 'Objective-C',
                 'Perl', 'PHP', 'Powershell', 'Python', 'R', 'Ruby', 'Rust', 'Sass', 'Scala', 'Scss', 'SQL', 'Swift',
                 'TSX', 'Typescript']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        # Check if lang is empty
        if lang == "Select Programming Language":
            messages.success(request, "Hey! You Forgot to Pick a Programming Language!")
            return render(request, 'suggest.html', {"lang_list": languages, "code": code, "lang": lang})
        else:
            # OpenAI Key
            openai.api_key = os.getenv('OPENAI_API_KEY')
            # OpenAI Instance
            openai.Model.list()

            try:
                response = openai.Completion.create(
                    model='gpt-3.5-turbo-instruct',
                    prompt=f"Respond only with code in the following language {lang}. {code}",
                    temperature=0,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0

                )
                # Response Parsing
                response = (response['choices'][0]['text']).strip()
                # Save to database
                record = Code(question=code, code_response=response, language=lang, user=request.user)
                record.save()
                return render(request, 'suggest.html', {"lang_list": languages, "response": response, "lang": lang})

            except Exception as e:
                return render(request, 'suggest.html', {"lang_list": languages, "code": e, "lang": lang})

        # return render(request, 'suggest.html', {"lang_list": languages, "code": code, "lang": lang})

    return render(request, 'suggest.html', {"lang_list": languages})


# User Login CBV
class CustomLoginView(LoginView):
    template_name = 'home.html'
    success_url = reverse_lazy('website:home')

    def form_valid(self, form):
        messages.success(self.request, "You have been loggedin successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = "home"
    template_name = 'register.html'


def past_code(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {"code": code})
    else:
        messages.success(request, "You Must Be Logged To View This Page!")
        return redirect('home')


class DeleteCodeView(DeleteView):
    model = Code
    success_url = reverse_lazy('past_code')
    template_name = "past.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        code = Code.objects.filter(user_id=self.request.user.id)
        context["code"] = code
        messages.success(request, "Deleted Successfully!")
        return context