import numpy as np
import pandas as pd
#LR,DTC,RF,GBDT,XGB,CAT,ETC,LGB,SVC,KNN,MLP
from sklearn.model_selection import KFold,cross_validate,LeaveOneOut,GridSearchCV
from sklearn.preprocessing  import StandardScaler
from sklearn.metrics import roc_auc_score,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from xgboost.sklearn import XGBClassifier
import random
import hyperopt
from hyperopt import hp, fmin, tpe, Trials, partial
from hyperopt.early_stop import no_progress_loss
import joblib

train = pd.read_csv('../CMC_HBCC_LIBD_Bloos_train_subsubset.csv',index_col=0).T
X_train = train.drop(columns='group')
y_train = train.group
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
random_state=30
k = 10
# 构造参数空间
param_grid_simple_lr = [
    { 'penalty': ['l1'], 'C': np.arange(0.1, 2, 0.1).tolist(), 'solver': ['saga'],'class_weight':[None, 'balanced']},
    { 'penalty': ['l2'], 'C': np.arange(0.1, 2, 0.1).tolist(), 'solver': ['lbfgs', 'newton-cg', 'sag', 'saga'],'class_weight':[None, 'balanced']},
    {'penalty': ['elasticnet'], 'C': np.arange(0.1, 2, 0.1).tolist(), 'l1_ratio': np.arange(0.1, 1, 0.1).tolist(), 'solver': ['saga'],'class_weight':[None, 'balanced']}
]
param_grid_simple_dt={"criterion": hp.choice("criterion",["gini","entropy"])
                                ,"max_depth": hp.quniform("max_depth",1,100,1)
                                ,'min_samples_split':hp.quniform("min_samples_split",2,100,1)
                                ,'min_samples_leaf':hp.quniform('min_samples_leaf',1,100,1)
                                ,"max_features": hp.quniform("max_features",1,184,1)
                                ,"min_impurity_decrease":hp.quniform("min_impurity_decrease",0,2,0.01)
                                 }
param_grid_simple_rf={'n_estimators': hp.quniform("n_estimators",10,200,1)
                    ,"criterion": hp.choice("criterion",["gini","entropy"])
                    ,"max_depth": hp.quniform("max_depth",3,20,1)
                    ,'min_samples_split':hp.quniform("min_samples_split",5,20,1)
                    ,'min_samples_leaf':hp.quniform('min_samples_leaf',5,10,1)
                    ,"max_samples": hp.quniform("max_samples",1,926,1)
                    ,"max_features": hp.quniform("max_features",1,184,1)
                    ,"min_impurity_decrease":hp.quniform("min_impurity_decrease",0,2,0.001)
                     }
param_grid_simple_svm={'C': hp.quniform("C",0.01,2,0.01)
                              ,"kernel": hp.choice("kernel",["rbf",'linear'])
                   ,'class_weight':hp.choice('class_weight',[None, 'balanced'])
                             ,"gamma" :hp.quniform("gamma",0.01,1,0.01)
                                                   }
param_grid_simple_gbdt={"learning_rate": hp.quniform("learning_rate",0.001,0.2,0.001)
                    ,'n_estimators': hp.quniform("n_estimators",20,200,1)
                    ,"subsample": hp.quniform("subsample",0.001,1,0.001)
                      ,"criterion": hp.choice("criterion",['friedman_mse', 'squared_error'])
                    ,'min_samples_split':hp.quniform("min_samples_split",5,10,1)
                    ,'min_samples_leaf':hp.quniform('min_samples_leaf',5,10,1)
                      ,"max_depth": hp.quniform("max_depth",1,6,1)
                       ,"max_features": hp.quniform("max_features",1,184,1)
                      ,"min_impurity_decrease":hp.quniform("min_impurity_decrease",0,2,0.01)
                                                       }
param_grid_simple_et={'n_estimators': hp.quniform("n_estimators",10,300,1)
                    ,"criterion": hp.choice("criterion",["gini","entropy"])
                    ,"max_depth": hp.quniform("max_depth",1,50,1)
                    ,'min_samples_split':hp.quniform("min_samples_split",2,20,1)
                    ,'min_samples_leaf':hp.quniform('min_samples_leaf',1,20,1)
                    ,"max_samples": hp.quniform("max_samples",0.01,1,0.01)
                    ,"max_features": hp.quniform("max_features",1,184,1)
                    ,"min_impurity_decrease":hp.quniform("min_impurity_decrease",0,2,0.001)
                     }
param_grid_simple_mlp={'activation':hp.choice('activation',['identity', 'logistic', 'tanh', 'relu'])
                                ,'alpha':hp.quniform('alpha',0.00001,0.001,0.00005)
                                ,'max_iter':hp.quniform('max_iter',200,500,5)
                                }
param_grid_simple_xgb = {'n_estimators': hp.quniform("n_estimators",30,200,1)
                  ,"lr": hp.quniform("learning_rate",0,1,0.01)
                  ,"booster": hp.choice("booster",['gbtree'])
                  ,"gamma":hp.quniform("gamma",0,7,0.01)
                  ,"max_depth": hp.quniform("max_depth",1,20,1)
                  ,"min_child_weight": hp.quniform("min_child_weight",2,5,0.1)
                  ,"subsample":hp.quniform("subsample",0,1,0.01)
                  ,"colsample_bytree":hp.quniform("colsample_bytree",0,1,0.01)
                  ,"colsample_bynode":hp.quniform("colsample_bynode",0,1,0.01)
                  ,"reg_lambda":hp.quniform("reg_lambda",1.5,4,0.01)
                 }


def hyperopt_objective(params):
    clf = DecisionTreeClassifier(criterion = params["criterion"]
                                          ,max_depth = int(params["max_depth"])
                                         ,min_samples_split = int(params['min_samples_split'])
                                         ,min_samples_leaf = int(params['min_samples_leaf'])
                                          ,max_features = int(params["max_features"])
                                          ,min_impurity_decrease = params["min_impurity_decrease"]
                                          ,random_state=random_state)
    cv = KFold(n_splits=k,shuffle=True,random_state=random_state)
    res = cross_validate(clf
                        ,X=X_train
                        ,y=y_train
                        ,cv=cv
                        ,n_jobs=16
                        ,scoring='accuracy')
    return -np.mean(res['test_score'])

def param_hyperopt(max_evals=3000):
    # 保存迭代过程
    trials = Trials()
    # 设置提前停止
    early_stop_fn = no_progress_loss(200)
    # 定义代理模型
    params_best = fmin(hyperopt_objective
                       , space=param_grid_simple
                       , algo=tpe.suggest
                       , max_evals=max_evals
                       , verbose=True
                       , trials=trials
                       , early_stop_fn=early_stop_fn
                       )
    # 打印最优参数，fmin会自动打印最佳分数
    print("\n", "\n", "best params: ", params_best,
          "\n")
    return params_best, trials



