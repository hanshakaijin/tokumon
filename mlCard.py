import pandas as pd
import numpy as np
import os
import re
import json
import itertools
import random

from sklearn.model_selection import train_test_split, KFold, cross_val_score, cross_validate
from sklearn.metrics import accuracy_score, f1_score
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

# LogisticRegression
from sklearn.linear_model import LogisticRegression

# SVM
from sklearn.svm import LinearSVC, SVC

# Bayes
from sklearn.naive_bayes import GaussianNB

# k-neighbor
from sklearn.neighbors import KNeighborsClassifier

# Decition Tree
from sklearn.tree import DecisionTreeClassifier

# randam forest, boosting
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
#import xgboost as xgb

# neural net
from sklearn.neural_network import MLPClassifier

class MlCard():
    def __init__(self):
        raw = pd.read_csv("./titanic/titanic passenger list.txt")
        self.target = raw['survived']
        features = raw.drop(['survived', 'ticket', 'cabin', 'name'], axis=1)

        # cabin pretreatment
        cabin_head = []
        for c in raw['cabin'].fillna(""):
            if re.match('^[A-Z]\d+$', c):
                cabin_head.append(re.match('^([A-Z])\d+$', c)[1])
            elif re.match('^F [A-Z]\d+$', c):
                cabin_head.append(re.match('^F ([A-Z])\d+$', c)[1])
            elif c!="":
                cabin_head.append(re.match('^([A-Z])', c)[1])
            else:
                cabin_head.append(np.nan)

        cabin_isodd  = []
        for c in raw['cabin'].fillna(""):
            if re.match('^[A-Z]\d+.*$', c):
                cabin_isodd.append(int(re.match('^[A-Z](\d+).*$', c)[1]) % 2 == 1)
            elif re.match('^[A-Z]\d* [A-Z]\d+.*$', c):
                cabin_isodd.append(int(re.match('^[A-Z]\d* [A-Z](\d+).*$', c)[1]) % 2 == 0)
            else:
                cabin_isodd.append(np.nan)     

        features['cabin_head'] = cabin_head
        features['cabin_isodd'] = cabin_isodd

        # name pretreatment
        name_honorific = []
        for c in raw['name'].fillna(""):
            if re.match('^[\w \-\']+, \w+\. .*', c):
                name_honorific.append(re.match('^[\w \-\']+, (\w+)\. .*', c)[1])
            else:
                name_honorific.append("Countess")
        features['name_honorific'] = name_honorific

        # fill NA
        features["age_fill_median"] = features["age"].fillna(features["age"].median())
        features["age"] = features["age"].fillna(0)

        features["fare_fill_median"] = features["fare"].fillna(features["fare"].median())
        features["fare"] = features["fare"].fillna(0)

        for f in ['embarked', 'home.dest', 'cabin_head', 'cabin_isodd', 'boat']:
            features[f + "_fill_median"] = features[f].fillna(features[f].mode()[0])

        # make dummies
        features['pclass'] = features['pclass'].astype('category')
        dummies_features = pd.get_dummies(features.loc[:,["pclass","sex","embarked",'home.dest','cabin_head', 'cabin_isodd', 'name_honorific', 'boat', "embarked_fill_median",'home.dest_fill_median','cabin_head_fill_median', 'boat_fill_median']], drop_first=True, dummy_na=True)
        self.dummies_features_labels = dummies_features.columns.values
        features = pd.concat([features, dummies_features], axis=1)

        self.features_type = features.copy()

        # to category type to int
        features['pclass'] = features['pclass'].cat.codes
        features['sex'] = features['sex'].astype('category').cat.codes
        features['home.dest'] = features['home.dest'].astype('category').cat.codes
        features['cabin_head'] = features['cabin_head'].astype('category').cat.codes
        features['cabin_isodd'] = features['cabin_isodd'].astype('category').cat.codes
        features['embarked'] = features['embarked'].astype('category').cat.codes
        features['name_honorific'] = features['name_honorific'].astype('category').cat.codes
        features['boat'] = features['boat'].astype('category').cat.codes

        for f in ['embarked', 'home.dest', 'cabin_head', 'cabin_isodd', 'boat']:
            features[f + "_fill_median"] = features[f + "_fill_median"].astype('category').cat.codes
        
        self.features = features
        self.clf_s = [
            LogisticRegression(max_iter=1000),
            SVC(C=100, kernel='rbf'),
            GaussianNB(),
            KNeighborsClassifier(n_neighbors=50,  weights='distance'),
            DecisionTreeClassifier(max_depth=5),
            RandomForestClassifier(max_depth=5, n_estimators = 100),
            GradientBoostingClassifier(max_depth=5,),
            MLPClassifier()
        ]

    # クロスバリデーションなし（テスト用）
    def calc_score(self, tokumons, algorithm):
        TRAIN_RATE = 0.6667
        train_features, test_features, train_target, test_target = train_test_split(self.features, self.target, train_size=TRAIN_RATE, random_state=1)
        self.clf_s[algorithm-1].fit(train_features.loc[:, tokumons], train_target)
        train_predict = self.clf_s[algorithm-1].predict(train_features.loc[:, tokumons])
        test_predict = self.clf_s[algorithm-1].predict(test_features.loc[:, tokumons])
        print(self.clf_s[algorithm-1].__class__.__name__ + ": " + str(accuracy_score(test_target, test_predict))+ " " + str(accuracy_score(train_target, train_predict)))

    # クロスバリデーションで計算（本番用）
    def calc_cv_score(self, tokumons, algorithm):
        kfold = KFold(n_splits=3, shuffle=True)
        score_funcs = [
            'accuracy',
            'precision',
            'recall',
            'f1'
        ]

        use_features_dummy = []
        for f in tokumons:
            if f.endswith('_dummy'):
                for ff in ["pclass","sex","embarked",'home.dest','cabin_head', 'cabin_isodd', 'name_honorific', 'boat', "embarked_fill_median",'home.dest_fill_median','cabin_head_fill_median', 'cabin_isodd_fill_median', 'boat_fill_median']:
                    if f == ff+"_dummy":
                        use_features_dummy.extend([n for n in self.dummies_features_labels if (n.startswith(ff) and not n.startswith(ff+"_fill_median"))])
                        break
                for ff in ["embarked_fill_median",'home.dest_fill_median','cabin_head_fill_median', 'cabin_isodd_fill_median', 'boat_fill_median']:
                    if f == ff+"_dummy":
                        use_features_dummy.extend([n for n in self.dummies_features_labels if n.startswith(ff)])
                        break
            else:
                use_features_dummy.append(f)

        result = cross_validate(self.clf_s[algorithm-1], self.features.loc[:, use_features_dummy], self.target, cv = kfold, scoring = score_funcs)
        score = {}
        #print(use_features_dummy)
        for s in score_funcs:
            #print(self.clf_s[algorithm-1].__class__.__name__ + ": " + str(result['test_' + s].mean()))
            score[s] = result['test_' + s].mean()
        return score
        
    # カードに記載する最大値などを算出する
    def show_describe(self):
        # categoly describe
        for f in ['pclass', 'sex', 'embarked', 'home.dest', 'cabin_head', 'cabin_isodd', 'name_honorific', 'boat']:
            print(f + ": ")
            print(self.features_type[f].value_counts())
            print("unique: " + str(self.features_type[f].nunique()))
            print("missing: " + str(self.features_type[f].isnull().sum() / len(self.features_type[f])))

        # number describe
        for f in ['age', 'sibsp', 'parch', 'fare']:
            print(f + ": ")
            print("min: " + str(self.features_type[f].min()))
            print("max: " + str(self.features_type[f].max()))
            print("missing: " + str(self.features_type[f].isnull().sum() / len(self.features_type[f])))

    #カードに記載する決定境界を描く
    def view_decision_boundaries(self):
        for i, clf in enumerate(self.clf_s):
            # describe model 
            print(clf)
            # plot descition boundary
            self.view_decision_boundary(self.features.loc[:, ['fare_fill_median', 'age_fill_median']], self.target, clf, i)

    def view_decision_boundary(self, x, y, clf, i):
        markers = ('x', 's')
        cmap = ListedColormap(('red', 'green'))

        x1_min, x1_max = x.iloc[:,0].min()-1, x.iloc[:,0].max()+1
        x2_min, x2_max = x.iloc[:,1].min()-1, x.iloc[:,1].max()+1
        x1_mesh, x2_mesh = np.meshgrid(np.arange(x1_min, x1_max, 1),
                                       np.arange(x2_min, x2_max, 1))

        clf.fit(x, y)
        z = clf.predict(np.array([x1_mesh.ravel(), x2_mesh.ravel()]).T)
        z = z.reshape(x1_mesh.shape)

        plt.figure(figsize=(16, 6))
        plt.contourf(x1_mesh, x2_mesh, z, alpha=0.5, cmap=cmap)
        plt.xlim(x1_mesh.min(), x1_mesh.max()/3)
        plt.ylim(x2_mesh.min(), x2_mesh.max())
        plt.tick_params(labelsize=42, length=20, width=5)

        for idx, cl in enumerate(np.unique(y)):
            plt.scatter(x=x.iloc[:, 0][y == cl],
                        y=x.iloc[:, 1][y == cl],
                        alpha=0.6,
                        c=cmap(idx),
                        s=16,
                        marker=markers[idx],
                        label=cl)
        plt.tight_layout()
        plt.savefig('./' + str(i+1) + '.png')

#ml = MlCard()
#ml.calc_cv_score(['pclass', 'sex_dummy', 'pclass',  'age_fill_median', 'sibsp'], 7)
