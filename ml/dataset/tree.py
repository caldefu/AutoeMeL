import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
import graphviz



def histrograma(df,col, n, x=2, y=2):
    fig=plt.figure(figsize=(x,y))
    plt.hist(df, bins = n, color="green")
    fig.savefig("".join(['./static/cache/hist',col,'.png']))
    fig.clear()

def imagen_feature_importances(atributos,valores):
    n=len(atributos)
    fig, ax = plt.subplots()
    y_pos = np.arange(n)
    ax.barh(y_pos, valores, align='edge',
        color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(atributos[:8])
    ax.set_xlabel('Importancia')
    ax.set_title('Importancia de los atributos en la clasificación')
    fig.savefig('./static/cache/features_importances.png')
    fig.clear()


def categorias_to_dummy (df):
    variables=df.columns.tolist()
    X=variables[0:-1]
    Y=variables[-1]
    
    categoricas = df[X].select_dtypes(include=["object","category"]).columns
    if len(categoricas) != 0:
        cat_dataframe = pd.get_dummies (df[categoricas], drop_first = True, dummy_na=False)
        df.drop(categoricas, axis=1, inplace=True)
        df = pd.concat([cat_dataframe, df], axis=1)
        variables=df.columns.tolist()
        X=variables[0:-1]        
    return df, X, Y
    



def imagen_correlations(dataframe, show_chart = True):
    fig = plt.figure(figsize = (12,6))
    corr = dataframe.corr()
    if show_chart == True:
        sns.heatmap(corr, 
                    xticklabels=corr.columns.values,
                    yticklabels=corr.columns.values,
                    annot=True)
    fig.savefig('./static/cache/corr.png')
    fig.clear()



def best_decision_tree (df, X, Y, max_profundidad_arbol=8):
    best_score=-1
    narboles=0
    for criterion in {"entropy", "gini"}:
        for splitter in {"best", "random"}:
            for i in range (2,max_profundidad_arbol):
                narboles += 1
                tree = DecisionTreeClassifier (criterion=criterion,
                                                splitter=splitter,
                                                max_depth=i,
                                                random_state=73,
                                                class_weight="balanced")
                tree.fit(df[X],df[Y])              
                cv= KFold (n_splits=10, shuffle=True, random_state=73)
                score=np.mean(cross_val_score(tree,df[X],df[Y],scoring="accuracy",cv=cv,n_jobs=2))
                if score>best_score:
                    best_score=score
                    best_criterion=criterion
                    best_max_depth=i
                    best_splitter=splitter
                    features_importance=tree.feature_importances_
                    arbol=export_graphviz(tree, 
                                out_file=None,
                                feature_names=X,
                                filled=True,
                                class_names=df[Y].unique().astype(str),
                                rounded=True,
                                special_characters=True)               
              
    return (best_score,
            best_criterion,
            best_max_depth,
            best_splitter,
            features_importance,
            narboles,
            arbol)
            