from tokenize import String
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pybedtools
import re
import streamlit as st
from pybedtools import BedTool
import shutil
import warnings

def main(tf : String):
    warnings.filterwarnings("ignore")

    alu_df = pybedtools.BedTool('data/a - Repeats')

    df_a = pd.read_table(alu_df.fn, names=['chrom', 'start', 'stop', 'name', 'score', 'strand'])

    tf_df = pybedtools.BedTool('data/b - TF')

    df_b = pd.read_table(tf_df.fn, names=['chrom', 'start', 'stop', 'name', 'score'])

    df_a = df_a[df_a['name'].str.startswith('Alu')]
    df_a.reset_index(drop=True, inplace=True)

    user_input_tf = tf

    df_b_new = df_b[df_b['name'].str.contains(user_input_tf)]
    df_b_new.reset_index(drop=True, inplace=True)

    df_a_bed = pybedtools.BedTool.from_dataframe(df_a)
    df_b_bed = pybedtools.BedTool.from_dataframe(df_b_new)

    c = df_a_bed.intersect(df_b_bed, wa=True)

    final_c_df = pd.read_table(c.fn, names=['chrom', 'start', 'stop', 'name', 'score', 'strand'])

    if os.path.isdir("plots"):
        os.chdir("./plots")
    else:
        os.mkdir("plots")
        os.chdir("./plots")    

    plt.figure(figsize=(10,10), dpi=420)
    plt.bar(final_c_df['name'], final_c_df['score'])
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.title('Transcription Factor ' + str(user_input_tf) + ' overlapping with Alu repeats')
    plt.savefig('Barplot.png')

    plt.figure(figsize=(10,10), dpi=420)
    sns.lineplot(final_c_df['name'], final_c_df['score'])
    plt.grid(True)
    plt.title('Transcription Factor ' + str(user_input_tf) + ' overlapping with Alu repeats')
    plt.xticks(rotation=90)
    plt.savefig('Lineplot.png')

    plt.figure(figsize=(10,10), dpi=420)
    sns.distplot(final_c_df['score'], hist=True, kde=True, kde_kws={'linewidth': 2})
    plt.grid(True)
    plt.title("Transcription Factor's " + str(user_input_tf) + ' density distribution of overlapping Alu repeats')
    plt.savefig('Distplot.png')

    plt.figure(figsize=(10,10), dpi=420)
    sns.countplot(final_c_df['chrom'], hue=final_c_df['name'])
    plt.title("Transcription Factor's " + str(user_input_tf) + ' presence on Alu repeats in different chromosomes')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.legend(loc = 'upper right')
    plt.savefig('Countplot.png')

    val_counts = final_c_df['chrom'].value_counts()

    plt.figure(figsize=(10,10), dpi=420)
    sns.barplot(val_counts.index, val_counts.values)
    plt.title("Transcription Factor's " + str(user_input_tf) + ' presence on Alu repeats')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.savefig('Barplot2.png')
    
    os.chdir("../")
