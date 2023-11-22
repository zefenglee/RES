rm(list = ls())
getwd()
setwd('F:/my projects/论文/论文三_精分/数据及分析/Paper 3/2nd_20230818/RFE code/CHLB_3packages_union(600)/subdata/main/')
options(stringsAsFactors = F)
library(reticulate)
library(clusterProfiler)
library(org.Hs.eg.db)
library(GSEABase)
library(ggplot2)
library(tidyverse)
library(readxl)
cutoff = '|0.5|'
Up_path = paste0('/home/data/t220336/Paper 3/2nd_20230818/DEA result/3Xpackages /union//',data,'/Up_Ensembl_IDs_Log2FCcutoff_' ,cutoff , '.RData')
load(Up_path)
Down_path = paste0('/home/data/t220336/Paper 3/2nd_20230818/DEA result/3Xpackages /union//',data,'/Down_Ensembl_IDs_Log2FCcutoff_' ,cutoff , '.RData')
load(Down_path)
DEGs<-c(Up_Ensembl_IDs_union,Down_Ensembl_IDs_union)
## ===GO数据库
np = import('numpy')
DEGs = np$load('cols_remain.npy') 
ego_CC <- data.frame(enrichGO(gene=DEGs, OrgDb= 'org.Hs.eg.db', keyType='ENSEMBL', ont="CC", pvalueCutoff= 0.05,qvalueCutoff= 0.05))
ego_MF <- data.frame(enrichGO(gene=DEGs, OrgDb= 'org.Hs.eg.db', keyType='ENSEMBL', ont="MF", pvalueCutoff= 0.05,qvalueCutoff= 0.05))
ego_BP <- data.frame(enrichGO(gene=DEGs, OrgDb= 'org.Hs.eg.db', keyType='ENSEMBL', ont="BP", pvalueCutoff= 0.05,qvalueCutoff= 0.05))
ego_CC$resource="CC"
ego_MF$resource="MF"
ego_BP$resource="BP"
## ===KEGG数据库
genelist<-bitr(gene = DEGs,fromType="ENSEMBL", toType="ENTREZID", OrgDb='org.Hs.eg.db')
genelist_ <- pull(genelist,ENTREZID)               
ekegg <- enrichKEGG(gene = genelist_, organism = 'hsa', pvalueCutoff = 0.05, qvalueCutoff = 0.05)
ekegg <- data.frame(ekegg)
ekegg$resource='KEGG'
a = c()
for(i in ekegg$geneID){
  geneids <- str_split(i,'/')[[1]]
  geneids_<- bitr(gene = geneids,fromType="ENTREZID", toType="ENSEMBL", OrgDb='org.Hs.eg.db')
  geneids_ <- pull(geneids_,ENSEMBL)  
  #print(geneids_)
  b <- paste0(geneids_,'/',collapse = '')
  a<-c(a,b)
  }
ekegg$geneID=a
pathways <-rbind(ego_BP,ego_CC,ego_MF,ekegg)
pathways <-na.omit(pathways)
save_path = paste0('GO&KEGG_Log2FCcutoff_' ,cutoff , '.csv')
write.table(pathways,save_path,sep=',')
print(dim(pathways))
