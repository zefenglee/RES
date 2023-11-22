rm(list = ls())
#设置文件路径
getwd()
setwd('F:/my projects/论文/论文三_精分/数据及分析/Paper 3/2nd_20230818/DEA result/DESeq2/LIBD/')
#载入包
library(limma)
library(edgeR)
library(stringr)
library(tidyverse)
library(DESeq2)
#载入数据
data<-read.csv('F:/my projects/论文/论文三_精分/数据及分析/Paper 3/2nd_20230818/data/LIBD_train.csv',row.names = 1)
#预处理数据
group_list <- data['group',]
k <- group_list==1
group_list[k]='SZ'
group_list[!k]='HS'
group_list <-factor(group_list,levels = c('SZ','HS'))
data<-data[-dim(data)[1],]
data<-data[rowSums(data==0)<=0.75*length(colnames(data)),]
data<-ceiling(data)
#差异分析
colData<-data.frame(row.names = colnames(data),condition=group_list)
dds<-DESeqDataSetFromMatrix(countData = data,colData = colData,design = ~condition)
dds$condition<-relevel(dds$condition,ref = 'HS')
dds<-DESeq(dds)
res<-results(dds,contrast = c('condition','SZ','HS'))
DEG<-as.data.frame(res)
colnames(DEG)=c("BaseMean","Log2FC","lfcSE","stat","P_Value","adj_P_Value" )
#定义筛选标准，输出表格
Log2_cutoff<-0
K_Up<-(DEG$P_Value<0.05)&(DEG$Log2FC>Log2_cutoff)
K_Down<-(DEG$P_Value<0.05)&(DEG$Log2FC< -Log2_cutoff)
DEG$Change='Normal'
DEG$Change[K_Up]='Up'
DEG$Change[K_Down]='Down'
write.table(DEG,'LIBD_Log2FCcutoff_0.csv',sep=',')

