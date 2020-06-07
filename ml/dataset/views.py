from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from .models import Dataset
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth import get_user_model
from .tree import *
import time

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

        
class UserDataset (LoginRequiredMixin, ListView):
    model = Dataset
    template_name='dataset/dataset_list.html'
    def get_queryset(self):
        try:
            self.dataset_user = Dataset.objects.filter(user=self.request.user)
           # self.dataset_user = User.objects.prefetch_related('datasets').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist :
            raise Http404
           

        else:
            return self.dataset_user

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['dataset_user'] = self.dataset_user
        return context

class DeleteDataset (LoginRequiredMixin, DeleteView):
    model = Dataset
    success_url = reverse_lazy ('dataset:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return  queryset.filter(user_id = self.request.user.id)




def detail(request, pk):
    dataset =  get_object_or_404(Dataset, id=pk)
    file = dataset.archivo
    if file.name.endswith('.csv'): 
        df=pd.read_csv(file)
    elif file.name.endswith('.xls'):
        df=pd.read_excel(file)

    else:
        return render(request,'dataset/dataset_detail.html',{'valid':'novalido'})
    col_eliminada=""
    #Eliminacion de las columna índice
    for columna in df.columns.tolist():
        if columna in('ID','Id','id','iD','PK','Pk','Pk', 'pk'):
            df=df.drop([columna], axis=1)
            col_eliminada=columna

    variables=df.columns.tolist()
    X=variables[0:-1]
    Y=variables[-1]
    nfilas=df.shape[0]
    ncolumnas=df.shape[1]
    filamedia=(int)(nfilas/2)
    data=df.iloc[np.r_[0:5,filamedia:(filamedia+5),-5:0]].to_html
    imagen_correlations(df)
    for col in variables:
        histrograma(df[col],col, (int)(nfilas/10))
    histrograma(df[Y],Y, (int)(nfilas/10), 3, 3)

    precision, best_criterion, best_max_depth, best_splitter, features_importances, narboles, arbol, tiempo_modelado = best_decision_tree(df,X,Y,ncolumnas)
    
    imagen_feature_importances (variables[0:-1],features_importances)

    precision = round(precision*100, 2) 
    tiempo_modelado = round(tiempo_modelado,3)
    ctx={'data':data,
        'fecha':dataset.created_at,
        'description':dataset.description,
        'nombre':dataset.name,
        'size':file.size,
        'download':dataset.archivo,
        'atributos':X,
        'var_objetivo':Y,
        'rows':nfilas,
        'columns':ncolumnas,
        'col_eliminada':col_eliminada,
        'precision':precision,
        'best_criterion':best_criterion,
        'bext_max_depth':best_max_depth,
        'tiempo':tiempo_modelado,
        'narboles':narboles,
        'best_splitter': best_splitter
        }
    return render(request,'dataset/dataset_detail.html',ctx)


