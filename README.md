# Integrated Transcriptome Analysis Reveals Novel Molecular Signatures for Schizophrenia Characterization
This repository contains a series of scripts used for differential expression analysis, pathway enrichment analysis, and modeling. These scripts are essential for analyzing gene expression data, identifying key pathways, and building predictive models. The scripts are organized as follows:

## Table of Contents
1. [Differential Expression Analysis (DEA)](#differential-expression-analysis-dea)
   - [1.1 limma_DEA_code.R](#11-limma_dea_coder)
   - [1.2 edgeR_DEA_code.R](#12-edger_dea_coder)
   - [1.3 DESeq2_DEA_code.R](#13-deseq2_dea_coder)
2. [Pathway Enrichment Analysis](#pathway-enrichment-analysis)
   - [2.1 GO&KEGG_pathway.R](#21-gokegg_pathwayr)
3. [Feature Selection and Modeling](#feature-selection-and-modeling)
   - [3.1 RFE.py](#31-rfepy)
   - [3.2 modeling.py](#32-modelingpy)
   
## Differential Expression Analysis (DEA)

Scripts in this section perform differential expression analysis on gene expression datasets using different packages:

### 1.1 limma_DEA_code.R
This script uses the **limma** package to perform differential expression analysis. Limma is commonly used for microarray and RNA-seq data analysis.

#### Usage
Run the script in R:
```R
Rscript limma_DEA_code.R
