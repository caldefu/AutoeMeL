from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import DatasetModel

from django.contrib.auth import get_user_model
User = get_user_model()


class CreateDataset (LoginRequiredMixin, CreateView):
    fields = ("name", "description")
    model = DatasetModel
    template_name = 'dataset/dataset_form.html'
    success_url = reverse_lazy('dataset:list')
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

        
class ListDataset (LoginRequiredMixin, ListView):
    models = DatasetModel