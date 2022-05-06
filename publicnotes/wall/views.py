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
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            return redirect(note)
    else:
        form = NoteForm()

    return render(request, 'wall/add_note_form.html', {"form": form})
