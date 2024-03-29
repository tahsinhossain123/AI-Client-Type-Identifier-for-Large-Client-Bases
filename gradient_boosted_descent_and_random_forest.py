# -*- coding: utf-8 -*-
"""Gradient Boosted Descent and Random Forest

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D9xnPD-od2jwjOZ1cSxxSI3ZlqPinF67
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess
import sys

from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['Entity_Type_Detector_Data_Set.csv']))

df.sample(10)

"""## pycld failed expirement as most entities where lables unknown"""

pip install -U pycld2
import pycld2 as pycld
print(pycld.ENCODINGS)
print(pycld.LANGUAGES)
df['langs_pycld'] = df['Entity Name'].apply(lambda x: [r[0] for r in pycld.detect(x)[2]])
df['langs_pycld'] = df['langs_pycld'].str[0]

df.sample(10)

df['langs_pycld'].unique()

df['langs_pycld'].value_counts()

"""## Alphabet Detector new column"""

def ad_col():
  subprocess.check_call([sys.executable, "-m", "pip", "install", "alphabet-detector"])
  from alphabet_detector import AlphabetDetector
  ad = AlphabetDetector()
  df['langs_ad'] = df['Entity Name'].apply(lambda x: [ad.detect_alphabet(x)])
  df['langs_ad'] = df['langs_ad'].str[0]
  df['langs_ad'] = [list(e) for e in df.langs_ad]
  df['langs_ad'] = df['langs_ad'].str[0]

ad_col()

df.sample(10)

df['langs_ad'].unique()

df['langs_ad'].value_counts()

#less specific but nothing left unkown

"""## hybrid failed experiment ( do not want to work with this tool for less technical reasons)"""

def first_elem_of_list(x):
  if isinstance(x,list):
    x = x[0]
  return x

def google_hybrid():
  subprocess.check_call([sys.executable, "-m", "pip", "install", "googletrans==3.1.0a0"])
  from googletrans import Translator
  tran = Translator(service_urls=['translate.googleapis.com'])
  temp1 = []
  for x in df['Entity Name']:
    temp1.append(x)
  temp = []
  for x in range(df.shape[0]):
    if df['langs_ad'].iloc[x] == 'LATIN' or df['langs_ad'].iloc[x] =='CJK' or df['langs_ad'].iloc[x] =='CYRILLIC':
      x1 = tran.detect(temp1[x])
      temp.append(x1.lang)
    else:
      temp.append(df['langs_ad'].iloc[x])
  df['hybrid'] = temp
  df['hybrid'] = df['hybrid'].apply(lambda x: first_elem_of_list(x))

  google_hybrid()

df.sample(10)

"""## tiny segmenter to detrmine length of cjk langs"""

def jap_count(entity):
  subprocess.check_call([sys.executable, "-m", "pip", "install", "tinysegmenter"])
  import tinysegmenter
  segmenter = tinysegmenter.TinySegmenter()
  l = segmenter.tokenize(entity)
  h_list = []
  word_count = len(l)
  for x in l:
    if len(x) == 1:
      e_hex = ord(x)
      h_list.append(hex(e_hex))
  symbols = ['0x3063','0x30c4','0x30fc','0x309b','0x3099','0x309c','0x309a','0x3005','0x4edd','0x30fd','0x30fe','0x309d','0x309e','0x3003','0x3031','0x3032','0x3033',
             '0x3035' ,'0x3034','0x3002','0x3001','0x30fb','0x30a0','0xff1d','0x3006','0x301c','0x2026','0x2025','0x30f6','0x2022','0x25e6','0xfe45','0xfe46','0x203b',
             '0xff0A','0x303d','0x3013','0x266a','0x266b','0x266c','0x2669','0x3007','0x300c','0x300d','0x300e','0x300f','0xff08','0xff09','0x3014','0x3015','0xff3b',
             '0xff3d','0xff5b','0xff5d','0xff5e','0xff60','0x3008','0x3009','0x300a','0x300b','0x3010','0x3011','0x3016','0x3017','0x3018','0x3019','0x301a','0x301b']	
  for y in h_list:
    if y in symbols:
      word_count = word_count -1
  return word_count

j_sub['count'] = j_sub['Entity Name'].apply(lambda x: jap_count(x))
for x in j_sub['Entity Name']:
  print(segmenter.tokenize(x))

j_sub

# TA Comments 

# The link below shows an approach to multilingual data. It may be a bit challenging to implement something similar to this given your data set but i would take this approach into consideration. 
# https://www.kaggle.com/code/rstogi896/text-classification-on-multilingual-data/notebook

# Understanding how xgboost works
# https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost-HowItWorks.html

df['langs_ad'].unique()

def space_split(entity):
  import re
  if entity[-1] == '.':
    entity = entity[:-1]
  e_list = re.split(",|\.|\-|\s",entity)
  if '' in e_list:
    e_list.remove('')
  if '-' in e_list:
    e_list.remove('-')
  return len(e_list)

g_sub= df.loc[df['langs_ad'] == 'GREEK']
g_sub

g_sub['wl'] = g_sub['Entity Name'].apply(lambda x: space_split(x))

g_sub

df['langs_ad'].unique()

s_sub= df.loc[df['langs_ad'] == 'MASCULINE']
s_sub

df.drop(index = 543,inplace = True)

df['langs_ad'].unique()

df['langs_ad'].unique()

#latin,greek,cyrilic,arabic,hebrew,devenagari,armenian,gorgian,loa,sinhala,thai are fine with white space removal
#CJK,hiragana,katakana,hangul,myanmar are charchiter sperated

def char_split(entity):
  import re
  res = re.sub(r'[^\w\s]', '', entity)
  #how to split string into indvidual chars
  return len(res)

char_split('上海綠地(融)資擔保有限公司')

c_sub= df.loc[df['langs_ad'] == 'CJK']
c_sub

def entity_length():
  wc = []
  for i in df.index:
    if df['langs_ad'][i] == 'LATIN' or df['langs_ad'][i] == 'ARABIC' or df['langs_ad'][i] == 'CYRILLIC' or df['langs_ad'][i] ==  'GREEK' or df['langs_ad'][i] == 'HEBREW' or df['langs_ad'][i] == 'DEVANAGARI' or df['langs_ad'][i] == 'ARMENIAN' or df['langs_ad'][i] == 'GEORGIAN'or df['langs_ad'][i] == 'LAO' or df['langs_ad'][i] == 'SINHALA' or df['langs_ad'][i] == 'THAI':
      wc.append(space_split(df['Entity Name'][i]))
    else:
      wc.append(char_split(df['Entity Name'][i]))
  df['length'] = wc

entity_length()

df.sample(20)

df['Entity Type'].value_counts()

# he question about punctuation is as fallows: what exactly are wee checking for? just commas?

def comma_present(Entity):
  if ',' in Entity:
    return True
  else:
    return False

df['comma'] = df['Entity Name'].apply(lambda x: comma_present(x))
df.sample(10)

def num_commas(entity):
  num = entity.count(',')
  return num

df['comma_num'] = df['Entity Name'].apply(lambda x: num_commas(x))
df.sample(10)

df['comma_num'].value_counts()

# we will stick with just checking for a comma being present as there are only 8 examples of there being more than 8 commas

def period_present(Entity):
  if '.' in Entity:
    return True
  else:
    return False

df['period'] = df['Entity Name'].apply(lambda x: period_present(x))
df.sample(10)

df['period'].value_counts()

import string
import re

punc = string.punctuation
punc

temp_punc = punc.replace('.', '')
new_punc =temp_punc.replace(',', '')
new_punc

def other_punc(Entity):
  for p in new_punc:
    if p in Entity:
      return True
  return False

df['other_punc'] = df['Entity Name'].apply(lambda x: other_punc(x))
df.sample(10)

df['other_punc'].value_counts()

# Commented out IPython magic to ensure Python compatibility.
CrosstabResult=pd.crosstab(index=df['Entity Type'],columns=df['comma'])
# %matplotlib inline 
CrosstabResult.plot.bar()

# Commented out IPython magic to ensure Python compatibility.
CrosstabResult=pd.crosstab(index=df['Entity Type'],columns=df['period'])
# %matplotlib inline 
CrosstabResult.plot.bar()

# Commented out IPython magic to ensure Python compatibility.
CrosstabResult=pd.crosstab(index=df['Entity Type'],columns=df['other_punc'])
# %matplotlib inline 
CrosstabResult.plot.bar()

# Commented out IPython magic to ensure Python compatibility.
CrosstabResult=pd.crosstab(index=df['Entity Type'],columns=df['length'])
# %matplotlib inline 
CrosstabResult.plot.bar()

import spacy
from spacy import displacy
spacy.blank('xx')
text = "Smartex International Ltd"

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
print(ents)

#just a thought but this may be somewhat helpful

df.sample(20)

#any time there is a char not in w (so yes in w), i want to return true

import sys
from unicodedata import category
 
 
punctuation_chars =  [
    chr(i) for i in range(sys.maxunicode)
    if category(chr(i)).startswith("P")
    ]

len(punctuation_chars)

new_punc_chars = ''.join(punctuation_chars).replace(',', '')
new_punc_chars

def other_punc_new(Entity):
  for p in new_punc_chars:
    if p in Entity:
      return True
  return False

df['other_punc'] = df['Entity Name'].apply(lambda x : other_punc_new(x))

df.head()



df['other_punc'].value_counts()

sub = df.loc[df['other_punc'] == True]
sub['langs_ad'].unique()

df['langs_ad'].unique()

# Commented out IPython magic to ensure Python compatibility.
CrosstabResult=pd.crosstab(index=df['Entity Type'],columns=df['other_punc'])
# %matplotlib inline 
CrosstabResult.plot.bar()

"""# Model Training"""

from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['df_f.csv']))

uploaded = files.upload()
dff = pd.read_csv(io.BytesIO(uploaded['dff.csv']))

df.head()

df.drop('langs_ad', axis = 1, inplace = True)

df.drop('Unnamed: 0', axis = 1, inplace = True)

df.head()

one_hot = pd.get_dummies(df['Entity Type'])
df = df.join(one_hot)

one_hot = pd.get_dummies(df['langs_ad'])
df = df.join(one_hot)

df.head()

y = df['Company']
X= df.drop(['Entity Type', 'Entity Name', 'Person', 'Company'], axis = 1)

X

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,stratify = dff['encoded_langs'])

from sklearn.ensemble import RandomForestClassifier

classyForest= RandomForestClassifier(n_estimators = 10000,max_depth =10)

classyForest.fit(X_train,y_train)
classyForest.score(X_test,y_test)

# increasing the number of estimators from 100 to 1000, didnt imporve perforance very much at all 0.8516
# i forogot to stratify, this helped. so now, 0.8572, done with max iter = 1000, max_depth = 15

# Maximum number of levels in tree
max_depth = [10,15,20,25,30,35]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [5,10,15]
# Method of selecting samples for training each tree
# Create the random grid
peram_grid = {
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.metrics import make_scorer
classyForest = RandomForestClassifier(random_state = 42)
roc_auc_scorer = make_scorer(roc_auc_score, greater_is_better=True,
                             needs_threshold=True)
gs = GridSearchCV(estimator=classyForest,
                  param_grid=peram_grid,
                  scoring=roc_auc_scorer,
                  cv=10,
                  n_jobs=-1)
gs.fit(X_train, y_train)
print("max roc_auc_score and hyperperam: ")
print(gs.best_score_)
print(gs.best_params_)

"""# Pause"""

classyForest = RandomForestClassifier(n_estimators = 10000, random_state = 42,  max_depth =  25, min_samples_leaf =  5, min_samples_split =  2)

classyForest.fit(X_train,y_train)
roc_auc_score(y_test, classyForest.predict_proba(X_test)[:,1])

from sklearn.metrics import confusion_matrix

y_pred = classyForest.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import precision_score

pr = precision_score(y_test, y_pred)

print(pr)

from sklearn.metrics import recall_score

r = recall_score(y_test, y_pred)
print(r)

from sklearn.metrics import f1_score

f = f1_score(y_test,y_pred)
print(f)

from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
sc.fit(X_train)
X_train_sc = sc.transform(X_train)
X_test_sc = sc.transform(X_test)

classyRegrassion= LogisticRegression()
classyRegrassion.fit(X_train_sc,y_train)
classyRegrassion.score(X_test_sc,y_test)

from sklearn.metrics import roc_auc_score

roc_auc_score(y_test, classyRegrassion.predict_proba(X_test)[:,1])

y_pred = classyRegrassion.predict(X_test_sc)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

from sklearn.preprocessing import PolynomialFeatures
trans = PolynomialFeatures(degree=2)
X_poly = trans.fit_transform(X)
X = pd.DataFrame(X_poly)

X_train,X_test,y_train,y_test = train_test_split(X,y,stratify = dff['encoded_langs'])
sc.fit(X_train)
X_train_sc = sc.transform(X_train)
X_test_sc = sc.transform(X_test)

classyRegrassion= LogisticRegression()
classyRegrassion.fit(X_train_sc,y_train)
classyRegrassion.score(X_test_sc,y_test)

y_pred = classyRegrassion.predict(X_test_sc)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

"""# pick up"""

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.metrics import make_scorer
grid = {'C': [.001,.01,.1,1,10,100]}
classyRegrassion= LogisticRegression(random_state = 42)
roc_auc_scorer = make_scorer(roc_auc_score, greater_is_better=True,
                             needs_threshold=True)
gs = GridSearchCV(estimator=classyRegrassion,
                  param_grid=grid,
                  scoring=roc_auc_scorer,
                  cv=10,
                  n_jobs=-1)
gs.fit(X_train_sc, y_train)
print("max roc_auc_score and hyperperam: ")
print(gs.best_score_)
print(gs.best_params_)

classyRegrassion= LogisticRegression(C = 100, random_state = 42)
classyRegrassion.fit(X_train_sc, y_train)

y_pred = classyRegrassion.predict(X_test_sc)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

gradient_booster = GradientBoostingClassifier(learning_rate=0.1)
gradient_booster.fit(X_train_sc,y_train)
print(classification_report(y_test,gradient_booster.predict(X_test_sc)))

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.metrics import make_scorer
grid = {'learning_rate': [.0001,.001,.01,.1, .2,.5], 'n_estimators': [100,500,1000], 'subsample': [.001,.01,.1,1]}
classyBooster = GradientBoostingClassifier(random_state = 42)
roc_auc_scorer = make_scorer(roc_auc_score, greater_is_better=True,
                             needs_threshold=True)
gs = GridSearchCV(estimator=classyBooster,
                  param_grid=grid,
                  scoring=roc_auc_scorer,
                  cv=10,
                  n_jobs=-1)
gs.fit(X_train_sc, y_train)
print("max roc_auc_score and hyperperam: ")
print(gs.best_score_)
print(gs.best_params_)

gradient_booster = GradientBoostingClassifier(learning_rate=0.2, n_estimators = 100, subsample = 1)
gradient_booster.fit(X_train_sc,y_train)
y_pred = gradient_booster.predict(X_test_sc)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

from hyperopt import tpe,hp,Trials
from hyperopt.fmin import fmin
from sklearn.metrics import mean_squared_error,make_scorer

seed=2
def objective(params):
    est=int(params['n_estimators'])
    md=int(params['max_depth'])
    msl=int(params['min_samples_leaf'])
    mss=int(params['min_samples_split'])
    model=RandomForestClassifier(n_estimators=est,max_depth=md,min_samples_leaf=msl,min_samples_split=mss)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    score=mean_squared_error(y_test,pred)
    return score

def optimize(trial):
    params={'n_estimators':hp.uniform('n_estimators',100,500),
           'max_depth':hp.uniform('max_depth',10,50),
           'min_samples_leaf':hp.uniform('min_samples_leaf',10,50),
           'min_samples_split':hp.uniform('min_samples_split', 10,20)}
    best=fmin(fn=objective,space=params,algo=tpe.suggest,trials=trial,max_evals=500,rstate=np.random.RandomState(seed))
    return best

trial=Trials()
best=optimize(trial)

print(best)

classyForest = RandomForestClassifier(max_depth =  30, min_samples_leaf =  10, min_samples_split =  20, n_estimators = 10000)

classyForest.fit(X_train,y_train)
roc_auc_score(y_test, classyForest.predict_proba(X_test)[:,1])

y_pred = classyForest.predict(X_test)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

seed=2
def objective(params):
    est=int(params['n_estimators'])
    md=int(params['max_depth'])
    msl=int(params['min_samples_leaf'])
    mss=int(params['min_samples_split'])
    model=RandomForestClassifier(n_estimators=est,max_depth=md,min_samples_leaf=msl,min_samples_split=mss)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    score=mean_squared_error(y_test,pred)
    return score

def optimize(trial):
    params={'n_estimators':hp.uniform('n_estimators',500,5000),
           'max_depth':hp.uniform('max_depth',20,150),
           'min_samples_leaf':hp.uniform('min_samples_leaf',10,30),
           'min_samples_split':hp.uniform('min_samples_split',5,20)}
    best=fmin(fn=objective,space=params,algo=tpe.suggest,trials=trial,max_evals=500,rstate=np.random.RandomState(seed))
    return best

trial=Trials()
best=optimize(trial)

print(best)

def objective(params):
    lr = (params['learning_rate'])
    md=int(params['max_depth'])
    ss=(params['subsample'])
    model=GradientBoostingClassifier(learning_rate = lr, subsample=ss,max_depth=md)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    score=mean_squared_error(y_test,pred)
    return score

def optimize(trial):
    params={'learning_rate':hp.choice('learning_rate',np.arange(0.05, 0.31, 0.05)),'subsample':hp.uniform('subsample', 0.8, 1),'max_depth': hp.choice('max_depth', np.arange(5, 16, 1))}
    best=fmin(fn=objective,space=params,algo=tpe.suggest,trials=trial,max_evals=500,rstate=np.random.RandomState(seed))
    return best

np.arange(0.05, 0.31, 0.05)

trial=Trials()
best=optimize(trial)

print(best)

gradient_booster = GradientBoostingClassifier(learning_rate=.15, max_depth = 10, subsample = .98)
gradient_booster.fit(X_train,y_train)

y_pred = gradient_booster.predict(X_test)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

roc_auc_score(y_test, gradient_booster.predict_proba(X_test)[:,1])

X_train.sample()

classyForest = RandomForestClassifier(n_estimators = 10000, random_state = 42,  max_depth =  25, min_samples_leaf =  5, min_samples_split =  2)
classyForest.fit(X_train,y_train)
y_pred = classyForest.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

imps = classyForest.feature_importances_
forest_importances = pd.Series(imps, X.columns)

forest_imps = {}
for c, i in zip(X_train.columns,imps):
  forest_imps[c] = i
sorted_imps = dict(reversed(sorted(forest_imps.items(), key=lambda item: item[1])))
print(sorted_imps)
j = 1
for k in sorted_imps:
  print(j, ": ", k, ": ", sorted_imps[k])
  j= j+1

cm = cm.round(2)


tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

fig = plt.figure(figsize=(8,8))
ax = sns.heatmap(cm, annot=True, cmap='Reds', fmt='g')
plt.title("Confusion Matrix of Best Random Forest")
plt.xlabel('Predicted')
plt.ylabel('Actual')

print('true-negitive:', tn, 
      '\nfalse-positive:', fp, 
      '\nfalse-negative:', fn, 
      '\ntrue-positive:', tp )

y_pred = classyForest.predict(X_test)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

gradient_booster = GradientBoostingClassifier(learning_rate=.2)
gradient_booster.fit(X_train,y_train)
y_pred = gradient_booster.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

cm = cm.round(2)


tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

fig = plt.figure(figsize=(8,8))
ax = sns.heatmap(cm, annot=True, cmap='Reds', fmt='g')
plt.title("Confusion Matrix of Best Gradient Boost")
plt.xlabel('Predicted')
plt.ylabel('Actual')

print('true-negitive:', tn, 
      '\nfalse-positive:', fp, 
      '\nfalse-negative:', fn, 
      '\ntrue-positive:', tp )

y_pred = gradient_booster.predict(X_test)
pr = precision_score(y_test, y_pred)
r = recall_score(y_test, y_pred)
f = f1_score(y_test,y_pred)
print("precition: ", pr, "recal: ", r, "f1: ", f)

