from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect  
from .models import Notes
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .forms import NotesForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class NotesDeleteView(LoginRequiredMixin,DeleteView):
    model = Notes
    success_url = '/notes' 
    template_name = 'notes/notes_delete.html'  # this is the template that will be used to display the delete confirmation page.
    login_url = '/admin'

class NotesUpdateView(LoginRequiredMixin,UpdateView):
    model = Notes
    success_url = '/notes' 
    form_class = NotesForm
    login_url = '/admin'

class NotesCreateView(LoginRequiredMixin,CreateView):
    model = Notes
    success_url = '/notes'  # this is the URL where the user will be redirected after a successful form submission.
    form_class = NotesForm
    login_url = '/admin'
    
    def form_valid(self, form):
        self.object = form.save(commit=False )
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url)
        
class NotesListView(LoginRequiredMixin,ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'
    login_url = '/admin'
    
    def get_queryset(self):
        return self.request.user.notes.all()
    
class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'  # this is the name of the variable in the template that will receive the note object.


def detail(request,pk):
    try:
        note = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/detail.html',{'note':note})