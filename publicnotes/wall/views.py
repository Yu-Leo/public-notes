import random

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

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
    context_object_name = 'notes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Note.objects.filter(category_id=self.kwargs['pk'])


class ViewAuthors(ListView):
    model = Author
    template_name = 'wall/authors_list.html'
    context_object_name = 'authors'
    allow_empty = False


class ViewAuthor(DetailView):
    model = Author
    template_name = 'wall/author.html'
    context_object_name = 'author'


def index(request):
    notes = Note.objects.all()
    context = {
        'notes': notes,
    }
    return render(request, 'wall/index.html', context)


def random_note(request):
    notes = Note.objects.all()
    if len(notes) > 0:
        return redirect(random.choice(notes))
    return redirect('home')


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
