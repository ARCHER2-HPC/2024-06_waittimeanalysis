#!/usr/bin/env python

# Script to read wait times by job size and produce plots and tables
# for analysis

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import weighted

# Set the num
nbins = 500

# Function to return the weighted distribution
def getdist(df, label):
    min = df['Wait Time / h'].min()
    max = df['Wait Time / h'].max()
    count = df['Jobs Run'].sum()
    usage = df['Raw Used'].sum()
    mean = sum(df['Wait Time / h'] * df['Raw Used']) / sum(df['Raw Used'])
    median = weighted.median(df['Wait Time / h'], df['Raw Used'])
    q1 = weighted.quantile(df['Wait Time / h'], df['Raw Used'], 0.25)
    q3 = weighted.quantile(df['Wait Time / h'], df['Raw Used'], 0.75)
    return label, min, q1, median, q3, max, mean, count, usage

# Function to return a weighted dataframe
def reindex_df(df, weight_col):
    """expand the dataframe to prepare for resampling
    result is 1 row per count per sample"""
    df = df.reindex(df.index.repeat(df[weight_col]))
    df.reset_index(drop=True, inplace=True)
    return(df)

# ### Wait time distributions

# ## Baseline (20 Mar - 3 Apr 2024)
df_allw_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/all_WaitTimeDistributionReport.csv')
df_e01w_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/e01_WaitTimeDistributionReport.csv')
df_e05w_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/e05_WaitTimeDistributionReport.csv')
df_e89w_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/e89_WaitTimeDistributionReport.csv')
df_exe05w_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/exe05_WaitTimeDistributionReport.csv')
df_epsrcw_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/EPSRC_WaitTimeDistributionReport.csv')
df_nercw_14dbl = pd.read_csv('data/2024-03-20_14d_baseline/NERC_WaitTimeDistributionReport.csv')
df_allw_14dbl['Series'] = 'All jobs'
df_allw_14dbl['Sample'] = 'Baseline'
df_e01w_14dbl['Series'] = 'UKTC (e01) jobs'
df_e01w_14dbl['Sample'] = 'Baseline'
df_e05w_14dbl['Series'] = 'MCC (e05) jobs'
df_e05w_14dbl['Sample'] = 'Baseline'
df_e89w_14dbl['Series'] = 'UKCP (e89) jobs'
df_e89w_14dbl['Sample'] = 'Baseline'
df_exe05w_14dbl['Series'] = 'All jobs (excl. MCC/e05)'
df_exe05w_14dbl['Sample'] = 'Baseline'
df_epsrcw_14dbl['Series'] = 'EPSRC jobs'
df_epsrcw_14dbl['Sample'] = 'Baseline'
df_nercw_14dbl['Series'] = 'NERC jobs'
df_nercw_14dbl['Sample'] = 'Baseline'

# Boxplot comparing wait times weighted by usage
plt.figure(figsize=(10,4))
df_temp = pd.concat([df_allw_14dbl, df_e01w_14dbl, df_e05w_14dbl, df_e89w_14dbl, df_exe05w_14dbl, df_epsrcw_14dbl, df_nercw_14dbl], ignore_index=True)
sns.boxplot(
        y="Series",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-wait-time_14dbl.png', bbox_inches='tight', dpi=300)

# Table of wait times weighted by usage
usage_stats = []
usage_stats.append(getdist(df_allw_14dbl, 'All jobs'))
usage_stats.append(getdist(df_e01w_14dbl, 'UKTC (e01) jobs'))
usage_stats.append(getdist(df_e05w_14dbl, 'MCC (e05) jobs'))
usage_stats.append(getdist(df_e89w_14dbl, 'UKCP (e89) jobs'))
usage_stats.append(getdist(df_exe05w_14dbl, 'All jobs (excl. MCC/e05)'))
usage_stats.append(getdist(df_epsrcw_14dbl, 'EPSRC jobs'))
usage_stats.append(getdist(df_nercw_14dbl, 'NERC jobs'))
df_usage = pd.DataFrame(usage_stats, columns=['Label', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'Mean', 'Jobs', 'Usage (CU)'])
print()
print("Wait time distribution (weighted by usage), baseline:")
print()
print(df_usage.to_markdown(index=False, floatfmt=".1f"))

# ## 6h half-life test (14 - 28 Apr 2024) 
df_allw_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/all_WaitTimeDistributionReport.csv')
df_e01w_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/e01_WaitTimeDistributionReport.csv')
df_e05w_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/e05_WaitTimeDistributionReport.csv')
df_e89w_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/e89_WaitTimeDistributionReport.csv')
df_exe05w_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/exe05_WaitTimeDistributionReport.csv')
df_epsrcw_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/EPSRC_WaitTimeDistributionReport.csv')
df_nercw_6hhl = pd.read_csv('data/2024-04-14_14d_6h-halflife/NERC_WaitTimeDistributionReport.csv')
df_allw_6hhl['Series'] = 'All jobs'
df_allw_6hhl['Sample'] = 'Expt. 1'
df_e01w_6hhl['Series'] = 'UKTC (e01) jobs'
df_e01w_6hhl['Sample'] = 'Expt. 1'
df_e05w_6hhl['Series'] = 'MCC (e05) jobs'
df_e05w_6hhl['Sample'] = 'Expt. 1'
df_e89w_6hhl['Series'] = 'UKCP (e89) jobs'
df_e89w_6hhl['Sample'] = 'Expt. 1'
df_exe05w_6hhl['Series'] = 'All jobs (excl. MCC/e05)'
df_exe05w_6hhl['Sample'] = 'Expt. 1'
df_epsrcw_6hhl['Series'] = 'EPSRC jobs'
df_epsrcw_6hhl['Sample'] = 'Expt. 1'
df_nercw_6hhl['Series'] = 'NERC jobs'
df_nercw_6hhl['Sample'] = 'Expt. 1'

df_temp = pd.concat([df_allw_6hhl, df_e01w_6hhl, df_e05w_6hhl, df_e89w_6hhl, df_exe05w_6hhl, df_epsrcw_6hhl, df_nercw_6hhl], ignore_index=True)
plt.figure(figsize=(10,4))
sns.boxplot(
        y="Series",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-wait-time_6hhl.png', bbox_inches='tight', dpi=300)

usage_stats = []
usage_stats.append(getdist(df_allw_6hhl, 'All jobs'))
usage_stats.append(getdist(df_e01w_6hhl, 'UKTC (e01) jobs'))
usage_stats.append(getdist(df_e05w_6hhl, 'MCC (e05) jobs'))
usage_stats.append(getdist(df_e89w_6hhl, 'UKCP (e89) jobs'))
usage_stats.append(getdist(df_exe05w_6hhl, 'All jobs (excl. MCC/e05)'))
usage_stats.append(getdist(df_epsrcw_6hhl, 'EPSRC jobs'))
usage_stats.append(getdist(df_nercw_6hhl, 'NERC jobs'))
df_usage = pd.DataFrame(usage_stats, columns=['Label', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'Mean', 'Jobs', 'Usage (CU)'])
print()
print("Wait time distribution (weighted by usage), 6-hour half-life:")
print()
print(df_usage.to_markdown(index=False, floatfmt=".1f"))


# ## Flat fair share tree test (9-22 May 2024)
df_allw_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/all_WaitTimeDistributionReport.csv')
df_e01w_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/e01_WaitTimeDistributionReport.csv')
df_e05w_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/e05_WaitTimeDistributionReport.csv')
df_e89w_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/e89_WaitTimeDistributionReport.csv')
df_exe05w_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/exe05_WaitTimeDistributionReport.csv')
df_epsrcw_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/epsrc_WaitTimeDistributionReport.csv')
df_nercw_flatfs = pd.read_csv('data/2024-05-09_14d_flattree/nerc_WaitTimeDistributionReport.csv')
df_allw_flatfs['Series'] = 'All jobs'
df_allw_flatfs['Sample'] = 'Expt. 2'
df_e01w_flatfs['Series'] = 'UKCP (e01) jobs'
df_e01w_flatfs['Sample'] = 'Expt. 2'
df_e05w_flatfs['Series'] = 'MCC (e05) jobs'
df_e05w_flatfs['Sample'] = 'Expt. 2'
df_e89w_flatfs['Series'] = 'UKCP (e89) jobs'
df_e89w_flatfs['Sample'] = 'Expt. 2'
df_exe05w_flatfs['Series'] = 'All jobs (excl. MCC/e05)'
df_exe05w_flatfs['Sample'] = 'Expt. 2'
df_epsrcw_flatfs['Series'] = 'EPSRC jobs'
df_epsrcw_flatfs['Sample'] = 'Expt. 2'
df_nercw_flatfs['Series'] = 'NERC jobs'
df_nercw_flatfs['Sample'] = 'Expt. 2'

df_temp = pd.concat([df_allw_flatfs, df_e01w_flatfs, df_e05w_flatfs, df_e89w_flatfs, df_exe05w_flatfs, df_epsrcw_flatfs, df_nercw_flatfs], ignore_index=True)
plt.figure(figsize=(10,4))
sns.boxplot(
        y="Series",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-wait-time_flatfs.png', bbox_inches='tight', dpi=300)

usage_stats = []
usage_stats.append(getdist(df_allw_flatfs, 'All jobs'))
usage_stats.append(getdist(df_e01w_flatfs, 'UKTC (e01) jobs'))
usage_stats.append(getdist(df_e05w_flatfs, 'MCC (e05) jobs'))
usage_stats.append(getdist(df_e89w_flatfs, 'UKCP (e89) jobs'))
usage_stats.append(getdist(df_exe05w_flatfs, 'All jobs (excl. MCC/e05)'))
usage_stats.append(getdist(df_epsrcw_flatfs, 'EPSRC jobs'))
usage_stats.append(getdist(df_nercw_flatfs, 'NERC jobs'))
df_usage = pd.DataFrame(usage_stats, columns=['Label', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'Mean', 'Jobs', 'Usage (CU)'])
print()
print("Wait time distribution (weighted by usage), flat fair share tree:")
print()
print(df_usage.to_markdown(index=False, floatfmt=".1f"))


# ## Comparisons

plt.figure(figsize=(10,4))
df_temp = pd.concat([df_allw_14dbl, df_allw_6hhl, df_allw_flatfs], ignore_index=True)
sns.boxplot(
        y="Sample",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-comparison_all.png', bbox_inches='tight', dpi=300)

plt.figure(figsize=(10,4))
df_temp = pd.concat([df_e05w_14dbl, df_e05w_6hhl, df_e05w_flatfs], ignore_index=True)
sns.boxplot(
        y="Sample",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-comparison_e05.png', bbox_inches='tight', dpi=300)


plt.figure(figsize=(10,4))
df_temp = pd.concat([df_e01w_14dbl, df_e01w_6hhl, df_e01w_flatfs], ignore_index=True)
sns.boxplot(
        y="Sample",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-comparison_e01.png', bbox_inches='tight', dpi=300)



plt.figure(figsize=(10,4))
df_temp = pd.concat([df_e89w_14dbl, df_e89w_6hhl, df_e89w_flatfs], ignore_index=True)
sns.boxplot(
        y="Sample",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-comparison_e89.png', bbox_inches='tight', dpi=300)



plt.figure(figsize=(10,4))
df_temp = pd.concat([df_nercw_14dbl, df_nercw_6hhl, df_nercw_flatfs], ignore_index=True)
sns.boxplot(
        y="Sample",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-comparison_nerc.png', bbox_inches='tight', dpi=300)

plt.figure(figsize=(10,4))
df_temp = pd.concat([df_exe05w_14dbl, df_exe05w_6hhl, df_exe05w_flatfs], ignore_index=True)
sns.boxplot(
        y="Sample",
        x='Wait Time / h',
        orient='h',
        showmeans=True,
        data=reindex_df(df_temp, weight_col='Raw Used')
        )
plt.xlim([0,196])
sns.despine()
plt.savefig('output/boxplot-comparison_exe05.png', bbox_inches='tight', dpi=300)





