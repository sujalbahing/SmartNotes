from django.shortcuts import render
from django.http import Http404  
from .models import Notes
from django.views.generic import CreateView, DetailView, ListView
from .forms import NotesForm
class NotesCreateView(CreateView):
    model = Notes
    success_url = '/notes'  # this is the URL where the user will be redirected after a successful form submission.
    form_class = NotesForm

class NotesListView(ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'
    
class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'  # this is the name of the variable in the template that will receive the note object.


def detail(request,pk):
    try:
        note = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/detail.html',{'note':note})