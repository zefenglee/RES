rm(list = ls())
#设置文件路径
getwd()
setwd('F:/my projects/论文/论文三_精分/数据及分析/Paper 3/2nd_20230818/DEA result//edgeR/LIBD/')
#载入包
library(limma)
library(edgeR)
library(stringr)
library(tidyverse)
#载入数据
data<-read.csv('../../../data/LIBD_train.csv',row.names = 1)
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
design<-model.matrix(~0+group_list)
colnames(design)=levels(group_list)
rownames(design)=colnames(data)
dge<-DGEList(counts = data,group = group_list)
dge<-calcNormFactors(dge)
dge <- estimateGLMCommonDisp(dge,design)
dge <- estimateGLMTrendedDisp(dge,design)
dge <- estimateGLMTagwiseDisp(dge,design)
fit<-glmFit(dge,design)
fit2<-glmLRT(fit,contrast = c(1,-1))
DEG<-topTags(fit2,n=Inf)
DEG<-DEG$table
colnames(DEG)=c("Log2FC","LogCPM","LR","P_Value","adj_P_Value" )
#定义筛选标准，输出表格
Log2_cutoff<-0
K_Up<-(DEG$P_Value<0.05)&(DEG$Log2FC>Log2_cutoff)
K_Down<-(DEG$P_Value<0.05)&(DEG$Log2FC< -Log2_cutoff)
DEG$Change='Normal'
DEG$Change[K_Up]='Up'
DEG$Change[K_Down]='Down'
table(DEG$Change)
write.table(DEG,'LIBD_Log2FCcutoff_0.csv',sep=',')

 
