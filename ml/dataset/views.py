from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from .models import Dataset
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .tree import *
from .forms import CreateDatasetForm
import time
import graphviz


User = get_user_model()


class CreateDataset (LoginRequiredMixin, CreateView):

    form_class = CreateDatasetForm
    model = Dataset
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



@login_required
def detail(request, pk):
    start = time.time()
    
    dataset =  get_object_or_404(Dataset, id=pk)
    fecha = dataset.created_at
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
        #Eliminacion de las filas con valores iguales a "?"
        df=df.drop(df[df[columna]=="?"].index)
        if columna in('ID','Id','id','iD','PK','Pk','Pk', 'pk'):
            df=df.drop([columna], axis=1)
            col_eliminada=columna



    #Eliminación de filas con valores vacíos.        
    df=df.dropna()

    #Conversión de atributos categoricos a numéricos mediante variables dummies.
    df,X,Y = categorias_to_dummy(df)
    nfilas=df.shape[0]
    ncolumnas=df.shape[1]
    filamedia=(int)(nfilas/2)
    data=df.iloc[np.r_[0:5,filamedia:(filamedia+5),-5:0]].to_html

    
    #Matriz de correlaciones      
    imagen_correlations(df)





    #Histogramas atributos
    n= (int)(nfilas/10)
    if n<5:
        n=4
    for col in X:
        histrograma(df[col],col,n)

    #Histograma clases
    clases=df[Y].unique().astype(str)
    histrograma(df[Y],Y, len(clases), 3, 3)


    if ncolumnas>8:
        max_depth=8
    else:
        max_depth=ncolumnas+1
   
    precision, best_criterion, best_max_depth,best_splitter,features_importances,narboles,arbol = best_decision_tree(df,X,Y, max_depth)
    
    
    imagen_feature_importances (X,features_importances)
    precision = round(precision*100, 2) 
    
    dataset.arbol=arbol
    dataset.save()
    end = time.time()
    
    tiempo_modelado= round(end-start, 3)
    ctx={'data':data,
        'fecha':fecha,
        'description':dataset.description_html,
        'nombre':dataset.name,
        'pk': dataset.id,
        'size':file.size,
        'clases': clases,
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

@login_required
def arbol(request, pk):
    dataset =  get_object_or_404(Dataset, id=pk)
    arbol = graphviz.Source(dataset.arbol,format='svg')
    arbol_pdf = graphviz.Source(dataset.arbol,format='pdf')
    arbol.render("./static/cache/arbol")
    arbol_pdf.render("./static/cache/arbol")
    ctx = {'name':dataset.name,'arbol':arbol}
    return render(request,'dataset/dataset_arbol.html',ctx)
