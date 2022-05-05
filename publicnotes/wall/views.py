import random

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView

from .models import Note


# Create your views here.

class ViewNote(DetailView):
    model = Note
    template_name = 'wall/note.html'
    context_object_name = 'note'


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
