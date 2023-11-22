# 基础数据科学运算库
import numpy as np
import pandas as pd

# 实用函数
from sklearn.metrics import accuracy_score,roc_auc_score

# 常用评估器
from sklearn.svm import SVC

# 其他模块
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import KFold,cross_validate
from sklearn.feature_selection import RFE

Train = pd.read_csv('../CMC_HBCC_LIBD_Bloos_train_subset.csv',index_col=0).T
Features = Train.drop(columns='group')
col_names = Features.columns
Labels = Train.group
scaler = StandardScaler()
Features = scaler.fit_transform(Features)
Features = pd.DataFrame(Features,columns=col_names)

validate_res_acc=[]
validate_res_auc=[]
cols_out = []
for i in tqdm(range(Features.shape[1])):
      
    i = Features.shape[1] - i
    if i<0:
        i=0
# 首次循环时，创建X_train_temp
    if i == Features.shape[1]:
        Features_temp=(Features).copy()
     
    #获得最优模型
        
    # 训练最优模型，然后带入RFE评估器
    clf = SVC(kernel='linear'
        ,probability=True
          ,random_state=30
          ,verbose=False)
    # clf = LogisticRegression(random_state=30,max_iter=1000)
    # clf = GradientBoostingClassifier(random_state=30)
    # clf = RandomForestClassifier(random_state=30)
    # clf = ExtraTreesClassifier(random_state=30)
    #最优模型交叉验证
    cv = KFold(n_splits=5,shuffle=True)
    validation_loss_acc = cross_validate(clf,Features_temp,Labels
                                    ,scoring="accuracy"
                                   ,cv=cv
                                     ,verbose=False
                                     ,n_jobs=-1
                                     ,error_score='raise')
    val_acc=np.mean(validation_loss_acc['test_score'])###
    
    validation_loss_auc = cross_validate(clf,Features_temp,Labels
                                    ,scoring="roc_auc"
                                   ,cv=cv
                                     ,verbose=False
                                     ,n_jobs=-1
                                     ,error_score='raise')
    val_auc=np.mean(validation_loss_auc['test_score'])###
    
    #RFE
    rfe_search = RFE(estimator=clf, n_features_to_select=i).fit(Features_temp, Labels)
    col_out=Features_temp.columns[rfe_search.ranking_ != 1]
    Features_temp=Features_temp.iloc[:,rfe_search.support_]

    # 搜索本轮被淘汰的特征，并记入rfe_res_search1
    ###
    validate_res_acc.append(val_acc)
    validate_res_auc.append(val_auc)
    cols_out.append(col_out)
pd.DataFrame({'acc':validate_res_acc,
             'auc':validate_res_auc,
             'cols_out':cols_out}).to_csv('rfe_svc_0.csv')