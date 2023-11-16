from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import DeleteView, ListView, FormView, DetailView
from .forms import SignUpForm, OpenAIForm
from .models import Code
import openai


class HomeView(FormView):
    template_name = 'home.html'
    form_class = OpenAIForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user_request = form.cleaned_data['user_request']
        language_selection = form.cleaned_data['language_selection']
        print(language_selection)

        openai.api_key = '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'

        try:
            response = openai.Completion.create(
                model='gpt-3.5-turbo-instruct',
                prompt=f"Respond only with code. Fix this {language_selection} code: {user_request}",
                temperature=0,
                max_tokens=2000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            code_generated = (response['choices'][0]['text']).strip()
        except Exception as e:
            code_generated = f"Error generating code: {str(e)}"

        record = Code(question=user_request, code_response=code_generated, language=language_selection,
                      user=self.request.user)
        record.save()

        context = self.get_context_data(form=form, code_generated=code_generated, language=language_selection)

        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class SuggestCodeView(FormView):
    template_name = 'suggest.html'
    form_class = OpenAIForm
    success_url = reverse_lazy('code_suggest')

    def form_valid(self, form):
        user_request = form.cleaned_data['user_request']
        language_selection = form.cleaned_data['language_selection']
        print(language_selection)

        openai.api_key = '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'

        try:
            response = openai.Completion.create(
                model='gpt-3.5-turbo-instruct',
                prompt=f"Respond only with code in the following language {language_selection} code: {user_request}",
                temperature=0,
                max_tokens=2000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            code_generated = (response['choices'][0]['text']).strip()
        except Exception as e:
            code_generated = f"Error generating code: {str(e)}"

        record = Code(question=user_request, code_response=code_generated, language=language_selection,
                      user=self.request.user)
        record.save()

        context = self.get_context_data(form=form, code_generated=code_generated, language=language_selection)

        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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


class PastCodeView(LoginRequiredMixin, ListView):
    template_name = 'past.html'
    model = Code

    def get_queryset(self, *args, **kwargs):
        qs = super(PastCodeView, self).get_queryset(*args, **kwargs)
        return qs.filter(user_id=self.request.user.id).order_by("-id")


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
