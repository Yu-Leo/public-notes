from django.shortcuts import render
from .models import Note
from django.views.generic import DetailView


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
