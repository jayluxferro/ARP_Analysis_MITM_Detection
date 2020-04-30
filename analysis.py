#!/usr/bin/python3

"""
Data Analysis
"""

import func as fx
import sys
import db
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import *

import logger as lg

# displaying a sample MLS sequence and the RTT
"""
binValue = []
RTT = []

for data in db.getTableScenarioCategory('incoming', fx.iterations, 1):
    for data2 in db.getTableScenarioCategorySeq('outgoing', data['scenario'], 1, data['seq']):
        binValue.append(data2['bin'])
        RTT.append(data['time'] - data2['time'])
x = np.linspace(1, len(binValue), len(binValue))

fig, ax1 = plt.subplots()
ax1.step(x, binValue)
ax1.set_ylabel('Amplitude')
ax1.set_xlabel('Sequence')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.legend(['MLS'])

ax2 = ax1.twinx()
ax2.plot(x, RTT, '-ro')
ax2.set_ylabel('Round Trip Time (s)')
ax2.tick_params(axis='y', labelcolor='r')
ax2.legend(['RTT'])
ax2.set_xticks(np.arange(len(x) + 1))
#ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
fig.tight_layout()
plt.grid(True, axis='both')
plt.show()
"""

# inits
dataset = pd.read_csv(fx.dataset, delimiter=',')
targets = dataset.iloc[:,1].values
inputs = dataset.iloc[:,[0]].values
class_names = ['Normal', 'MITM']

def generateResults(random_state=20):
    X_train, X_test, y_train, y_test = train_test_split(inputs, targets, test_size=0.2, random_state=random_state)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    
    model = LinearSVC(random_state=0).fit(X_train, y_train)
    print(model)
    lg.success('LinearSVC: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('Linear SVC - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()


    model = SVC(random_state=0).fit(X_train, y_train)
    print(model)
    lg.success('SVC: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('SVC - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()

    model = KNeighborsClassifier(n_neighbors=1).fit(X_train, y_train)
    print(model)
    lg.success('KNN: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('KNN - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()

    model = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
    print(model)
    lg.success('DecisionTree: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('Decision Tree - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()

    model = LogisticRegression(random_state=0).fit(X_train, y_train)
    print(model)
    lg.success('LogisticRegression: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('Logistic Regression - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()
    
    model = RandomForestClassifier(random_state=0).fit(X_train, y_train)
    print(model)
    lg.success('RandomForest: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('Random Forest - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()

    model = GradientBoostingClassifier(random_state=0).fit(X_train, y_train)
    print(model)
    lg.success('GradientBoosting: {:.2f}\n'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('Gradient Boosting - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()
    
    model = GaussianNB().fit(X_train, y_train)
    print(model)
    lg.success('GaussianNB: {:.2f}'.format(model.score(X_test, y_test)))
    plot_confusion_matrix(model, X_test, y_test, normalize='true', display_labels=class_names, cmap=plt.cm.Blues)
    #plt.title('Gaussian NB - {:.2f}%'.format(model.score(X_test, y_test)))
    plt.show()

# generate linear model results
generateResults(random_state=20)
