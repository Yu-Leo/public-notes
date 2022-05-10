import random

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login, logout

from .models import *
from .forms import *


# Create your views here.

class ViewNote(DetailView):
    model = Note
    template_name = 'wall/note.html'
    context_object_name = 'note'


class ViewCategory(ListView):
    model = Category
    template_name = 'wall/category.html'
    allow_empty = False
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Note.objects.filter(category_id=self.kwargs['pk']).select_related('category', 'author')


class ViewAuthors(ListView):
    model = Author
    template_name = 'wall/authors_list.html'
    context_object_name = 'authors'
    allow_empty = False


class ViewAuthor(DetailView):
    model = Author
    template_name = 'wall/author.html'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewAuthor, self).get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(author=self.kwargs['pk'])
        return context


def index(request):
    notes = Note.objects.all().select_related('category', 'author')
    paginator = Paginator(notes, 5)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    context = {
        'page_obj': page_objects
    }
    return render(request, 'wall/index.html', context)


def random_note(request):
    notes = Note.objects.all()
    if len(notes) > 0:
        return redirect(random.choice(notes))
    return redirect('home')


@login_required(login_url=reverse_lazy('login'))
def add_note(request):
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        author_form = AuthorForm(request.POST)

        if note_form.is_valid() and author_form.is_valid():
            notes_data = note_form.cleaned_data
            author = author_form.save()

            notes_data['author'] = author
            note = Note.objects.create(**notes_data)
            return redirect(note)
    else:
        note_form = NoteForm()
        author_form = AuthorForm()

    return render(request, 'wall/add_note_form.html', {"note_form": note_form, "author_form": author_form})


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'wall/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request, 'wall/login.html', context)


def about(request):
    return render(request, 'wall/about.html', {})
