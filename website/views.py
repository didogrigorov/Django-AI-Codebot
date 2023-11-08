import os
from django.contrib import messages
from django.shortcuts import render, redirect
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
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


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Great! You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "Wrong username or password! Please try again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out! Have a nice day!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')

    else:
        form = SignUpForm

    return render(request, 'register.html', {"form": form})


def past_code(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {"code": code})
    else:
        messages.success(request, "You Must Be Logged To View This Page!")
        return redirect('home')


def delete_snippet(request, id):
    previous = Code.objects.get(pk=id)
    previous.delete()
    messages.success(request, "Deleted Successfully!")
    return redirect('past_code')
