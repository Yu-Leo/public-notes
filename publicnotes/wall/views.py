from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView

from . import exceptions
from . import forms
from . import models
from . import services
from . import utils


def index(request):
    """Main page with all notes"""

    notes = services.get_all_notes()
    paginator = Paginator(notes, 5)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    context = {
        'page_obj': page_objects
    }
    '''
    send_mail(subject='Subject',
              message='Some text',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=['levayu22@gmail.com'],
              fail_silently=False)
    '''
    return render(request, 'wall/index.html', context)


class ViewNote(DetailView):
    """View note at single page"""

    model = models.Note
    template_name = 'wall/note.html'
    context_object_name = 'note'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(ViewNote, self).get_context_data(**kwargs)
        context['allow_edit'] = self.request.user == self.object.author  # Is authenticated user show his note?
        services.increase_number_of_views(self.object)
        return context


def random_note(request):
    """
    Page for redirecting user to random note.
    If there are no notes, redirect to home page.
    """

    try:
        return redirect(services.get_random_note())
    except exceptions.ThereAreNoNotes:
        return redirect('home')


@login_required(login_url=reverse_lazy('login'))
def add_note(request):
    """Page for creating note"""

    if request.method == 'POST':
        note_form = forms.NoteForm(request.POST)
        if note_form.is_valid():
            note = services.add_note(note_form, request.user)
            return redirect(note)
    elif request.method == 'GET' and request.GET.get('category') is not None:
        category_pk = int(request.GET.get('category'))
        try:
            note_form = forms.NoteForm(
                initial={'category': services.get_category_by_pk(category_pk)})
        except models.Category.DoesNotExist:
            note_form = forms.NoteForm()
    else:
        note_form = forms.NoteForm()

    return render(request, 'wall/add_note_form.html', {"note_form": note_form})


@login_required(login_url=reverse_lazy('login'))
def edit_note(request, pk: int):
    """Page for editing note"""

    if not services.is_authenticated_user_the_author_of_note(authenticated_user=request.user,
                                                             note_pk=pk):
        return redirect('login')

    if request.method == 'POST':
        note_form = forms.UpdateNote(request.POST,
                                     instance=services.get_note_by_pk(pk))
        if note_form.is_valid():
            note = note_form.save()
            return redirect(note)
    else:
        note_form = forms.UpdateNote(instance=services.get_note_by_pk(pk))

    context = {'note_form': note_form,
               'note_pk': pk}

    return render(request, 'wall/edit_note.html', context)


@login_required(login_url=reverse_lazy('login'))
def delete_note(request, pk):
    """Page for deleting note"""

    if not services.is_authenticated_user_the_author_of_note(authenticated_user=request.user,
                                                             note_pk=pk):
        return redirect('login')

    services.delete_note_by_pk(pk)
    messages.success(request, 'Заметка успешно удалена!')
    return redirect(request.user)


class ViewCategory(ListView):
    """View all notes and subcategories for category"""

    model = models.Category
    template_name = 'wall/category.html'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(ViewCategory, self).get_context_data(**kwargs)
        try:
            category = services.get_category_by_pk(self.kwargs['pk'])
            context['category'] = category
            context['categories_tree'] = services.get_ancestors_of_category(category)
            context['children'] = services.get_children_of_category(category)
            return context
        except models.Category.DoesNotExist:
            raise Http404()

    def get_queryset(self) -> list[models.Note]:
        """
        :return: list of notes, which belong to this category
        """
        try:
            return services.get_notes_from_category(category_pk=self.kwargs['pk'])
        except models.Category.DoesNotExist:
            raise Http404()


class ViewCategoriesList(ListView):
    """View list of categories"""

    model = models.Category
    template_name = 'wall/categories_list.html'
    context_object_name = 'categories'
    allow_empty = False


class ViewTag(ListView):
    """View all notes, which have this tag"""

    model = models.Tag
    template_name = 'wall/tag.html'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewTag, self).get_context_data(**kwargs)
        try:
            context['tag'] = services.get_tag_by_pk(self.kwargs['pk'])
            return context
        except models.Tag.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        try:
            return services.get_notes_by_tag(tag_pk=self.kwargs['pk'])
        except models.Tag.DoesNotExist:
            raise Http404()


class ViewAuthors(ListView):
    """View list of users"""

    model = models.User
    template_name = 'wall/authors_list.html'
    context_object_name = 'authors'
    allow_empty = False


class ViewAuthor(DetailView):
    """View user's profile"""

    model = models.User
    template_name = 'wall/author.html'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewAuthor, self).get_context_data(**kwargs)
        context['page_obj'] = services.get_notes_by_author(author_pk=self.kwargs['pk'])
        context['is_self'] = self.request.user == self.object  # Is authenticated user show his profile?
        return context


def registration(request):
    """Registration page"""

    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            services.register_user(form, domain=utils.get_current_domain(request))
            messages.warning(request, 'На указанный вами E-mail отправлено письмо с ссылкой для подтверждения')
            return redirect('home')
        messages.error(request, 'Ошибка регистрации')
    else:
        form = forms.UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'wall/registration.html', context)


def activate_user(request, uidb64: str, token: str):
    try:
        user = services.activate_user_by_link(uidb64, token)
        login(request, user)
        messages.success(request, 'E-mail успешно подтверждён')
        return redirect(user)
    except exceptions.UserActivationError:
        messages.error(request, 'Ошибка подтверждения E-mail')
        return redirect('home')


@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
    """Page for editing user's profile"""

    if request.method == 'POST':
        user_form = forms.UpdateProfile(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(request.user)
    else:
        user_form = forms.UpdateProfile(instance=request.user)

    return render(request, 'wall/edit_profile.html', {"user_form": user_form})


def user_login(request):
    """Login page"""

    if request.method == 'POST':
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = forms.UserLoginForm()

    context = {
        'form': form,
    }

    return render(request, 'wall/login.html', context)


@login_required(login_url=reverse_lazy('login'))
def change_password(request):
    """Page for changing user's password"""

    if request.method == 'POST':
        form = forms.UserChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пароль успешно сменён!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = forms.UserChangePasswordForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'wall/change_password.html', context)


@login_required(login_url=reverse_lazy('login'))
def delete_profile(request):
    """Page for delete user"""

    user = request.user
    logout(request)
    services.delete_user(user)
    messages.success(request, 'Профиль и заметки успешно удалены!')
    return redirect('home')


def user_logout(request):
    """Logout page"""

    logout(request)
    messages.error(request, 'Вы вышли из аккаунта')
    return redirect('login')


def handle_page_not_found(request, exception=None):
    """Handler for 404 error"""

    return render(request, 'wall/404.html', {})


class Search(ListView):
    """View result of search"""

    template_name = 'wall/search.html'
    paginate_by = 5

    def get_queryset(self):
        """
        :return: list of notes, which meets the search criteria
        """
        return services.search_note_by_title(title=self.request.GET.get('search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return context


class About(TemplateView):
    """Page with info about this project"""

    template_name = 'wall/about.html'
