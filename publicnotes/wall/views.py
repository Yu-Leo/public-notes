import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView

from .forms import *


# Create your views here.

class ViewNote(DetailView):
    model = Note
    template_name = 'wall/note.html'
    context_object_name = 'note'


class ViewCategory(ListView):
    model = Category
    template_name = 'wall/category.html'
    allow_empty = True
    paginate_by = 5

    def get_breadcrumb_list(self, category):
        breadcrumb_list = []
        while category:
            breadcrumb_list.append(category)
            category = category.parent
        return list(reversed(breadcrumb_list))[:-1]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewCategory, self).get_context_data(**kwargs)
        try:
            category = Category.objects.get(pk=self.kwargs['pk'])
            context['category'] = category
            context['categories_tree'] = self.get_breadcrumb_list(category)
            context['children'] = category.get_children()
            return context

        except Category.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        try:
            return Note.objects.filter(category_id=self.kwargs['pk']).select_related('category', 'author')
        except Category.DoesNotExist:
            raise Http404()


class ViewAuthors(ListView):
    model = User
    template_name = 'wall/authors_list.html'
    context_object_name = 'authors'
    allow_empty = False


class ViewAuthor(DetailView):
    model = User
    template_name = 'wall/author.html'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewAuthor, self).get_context_data(**kwargs)
        context['page_obj'] = Note.objects.filter(author=self.kwargs['pk'])
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
        if note_form.is_valid():
            notes_data = note_form.cleaned_data
            author = request.user
            notes_data['author'] = author
            note = Note.objects.create(**notes_data)
            return redirect(note)
    elif request.method == 'GET' and request.GET.get('category') is not None:
        category_pk = int(request.GET.get('category'))
        category_pk = category_pk
        try:
            note_form = NoteForm(initial={'category': Category.objects.get(pk=category_pk)})
        except Category.DoesNotExist:
            note_form = NoteForm()
    else:
        note_form = NoteForm()

    return render(request, 'wall/add_note_form.html', {"note_form": note_form})


@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateProfile(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(request.user)
    else:
        user_form = UpdateProfile(instance=request.user)

    return render(request, 'wall/edit_profile.html', {"user_form": user_form})


@login_required(login_url=reverse_lazy('login'))
def edit_note(request, pk):
    if request.user != Note.objects.get(pk=pk).author:
        return redirect('login')

    if request.method == 'POST':
        note_form = UpdateNote(request.POST, instance=Note.objects.get(pk=pk))
        if note_form.is_valid():
            note = note_form.save()
            return redirect(note)
    else:
        note_form = UpdateNote(instance=Note.objects.get(pk=pk))

    context = {'note_form': note_form,
               'note_pk': pk}

    return render(request, 'wall/edit_note.html', context)


@login_required(login_url=reverse_lazy('login'))
def delete_note(request, pk):
    note = Note.objects.get(pk=pk)

    if request.user != note.author:
        return redirect('login')

    note.delete()
    messages.success(request, 'Заметка успешно удалена!')
    return redirect(request.user)


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
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


@login_required(login_url=reverse_lazy('login'))
def change_password(request):
    if request.method == 'POST':
        form = UserChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Пароль успешно сменён!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserChangePasswordForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'wall/change_password.html', context)


def user_logout(request):
    logout(request)
    messages.error(request, 'Вы вышли из аккаунта')
    return redirect('login')


class About(TemplateView):
    template_name = 'wall/about.html'


def handle_page_not_found(request, exception=None):
    return render(request, 'wall/404.html', {})


@login_required(login_url=reverse_lazy('login'))
def delete_profile(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Профиль и заметки успешно удалены!')
    return redirect('home')


def categories_list(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория добавлена')
            return redirect('categories_list')
        else:
            messages.error(request, 'Ошибка добавления')
    else:
        form = CategoryForm()

    objects = Category.objects.all()

    context = {
        'form': form,
        'page_obj': objects
    }

    return render(request, 'wall/categories_list.html', context)


class Search(ListView):
    template_name = 'wall/search.html'
    paginate_by = 5

    def get_queryset(self):
        return Note.objects.filter(title__icontains=self.request.GET.get('search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return context
