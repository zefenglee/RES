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
```

### 1.2 edgeR_DEA_code.R
This script utilizes the edgeR package for differential expression analysis, ideal for RNA-seq count data, especially for datasets with varying sequencing depths.

#### Usage
Run the script in R:

```R
Rscript edgeR_DEA_code.R
```

### 1.3 DESeq2_DEA_code.R
The DESeq2 package is another powerful tool for differential expression analysis of RNA-seq data, focusing on count-based data normalization.

#### Usage
Run the script in R:

```R
Rscript DESeq2_DEA_code.R
```

## Pathway Enrichment Analysis
### 2.1 GO&KEGG_pathway.R
This script performs Gene Ontology (GO) and KEGG pathway enrichment analyses based on differential expression results. It helps identify key biological processes and pathways associated with gene expression changes.

#### Usage
Run the script in R:

```R
Rscript GO&KEGG_pathway.R
```
## Feature Selection and Modeling
### 3.1 RFE
The RFE.py script uses Recursive Feature Elimination (RFE) to select the most relevant features for building predictive models. RFE helps reduce the number of features by recursively removing the least important features.

#### Usage
Run the script in Python:

```bash
python RFE.py
```

### 3.2 modeling
This script builds predictive models based on the selected features. Various machine learning models can be trained and evaluated to predict specific outcomes based on gene expression data.

#### Usage
Run the script in Python:

```bash
python modeling.py
```
## Requirements
Each script has specific requirements:

R scripts require the respective R packages (limma, edgeR, DESeq2, and others for GO/KEGG analysis).
Python scripts require machine learning libraries (e.g., scikit-learn, pandas).
Install R packages from CRAN or Bioconductor as needed:

```R
install.packages("limma")
install.packages("edgeR")
install.packages("DESeq2")
```
For Python, install required packages using pip:

```bash
pip install scikit-learn pandas
```
## License
This repository is licensed under the MIT License.
