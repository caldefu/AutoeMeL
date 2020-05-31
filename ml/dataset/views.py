from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import Dataset
from .forms import DatasetForm
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()


class CreateDataset (LoginRequiredMixin, CreateView):
    model = Dataset
    fields = ("name", "description", "archivo")
    template_name = 'dataset/dataset_form.html'
    success_url = reverse_lazy('dataset:list')
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

        
class UserDataSets (LoginRequiredMixin, ListView):
    model = Dataset
    template_name='dataset/dataset_list.html'
    def get_queryset(self):
        try:
            self.dataset_user = Dataset.objects.filter(user=self.request.user)
           # self.dataset_user = User.objects.prefetch_related('datasets').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist :
            raise Http404
            print("noexiste")

        else:
            return self.dataset_user

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['dataset_user'] = self.dataset_user
        return context