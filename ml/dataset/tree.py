import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier


def histrograma(df,col, n, x=2, y=2):
    fig=plt.figure(figsize=(x,y))
    plt.hist(df, bins = n,color="green")
    fig.savefig("".join(['./static/cache/hist',col,'.png']))


def best_decision_tree(dataframe, X,Y):
    clf = DecisionTreeClassifier(random_state=0)
    print(cross_val_score(clf, dataframe[X], dataframe[Y], cv=10))

def imagen_correlations(dataframe, show_chart = True):
    fig = plt.figure(figsize = (12,6))
    corr = dataframe.corr()
    if show_chart == True:
        sns.heatmap(corr, 
                    xticklabels=corr.columns.values,
                    yticklabels=corr.columns.values,
                    annot=True)
    fig.savefig('./static/cache/corr.png')