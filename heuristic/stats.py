import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_header_page(text):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    plt.axis('off')
    ax.set(ylim=(-1, 1))
    ax.set(xlim=(-1, 1))
    ax.text(0, 0, text,horizontalalignment='center',verticalalignment='center', fontsize = 30)
    return fig

def generate_dataframes(save_path):
    params_df = {}
    gen = 0
    while gen >= 0:
        try:
            filename = f"{save_path}/gen{gen}.json"
            with open(filename) as f:
                listObj = json.load(f)
                nb_ind = len(listObj['gen'])
                for ind in range(nb_ind):
                    for param in range(len(listObj['gen'][ind]['parameters'])):
                        if param not in params_df:
                            params_df[param] = pd.DataFrame()
                        params_df[param].loc[gen, ind] = listObj['gen'][ind]['parameters'][param]
            gen += 1
        except:
            gen = -1

    return params_df.copy()

def plot_param_evolution(df, param, function_name=None):
    nb_gen, nb_ind = df[param].shape
    x_ticks = np.arange(0, nb_gen, 1)

    fig=plt.figure()
    ax=fig.add_subplot(111)


    var = df[param].var(axis=1)
    mean = df[param].mean(axis=1)
    for ind in range(nb_ind):
        ax.plot(df[param].index, df[param].iloc[:, ind], c='#666', linewidth=.5, label=None, fillstyle='none')

    ax.plot(df[param].index, var, c='#FA5', label=f"Diversity", fillstyle='none')
    ax.plot(df[param].index, mean, c='#3AD', linewidth=2, label=f"Mean value", fillstyle='none', marker="+", markersize=10)

    ax.set(title=f"Evolution of the parameter {param} {'used for '+function_name if function_name else ''}", xlabel='Generation', ylabel='Parameter value', xticks=x_ticks)
    ax.set_xticklabels(x_ticks, rotation=45)
    ax.add_line(plt.axhline(y=0, color='grey', linestyle='--'))
    ax.set(ylim=(-1, 1))
    ax.set(xlim=(0, nb_gen-1))
    ax.text(nb_gen-1.1, mean[nb_gen-1], round(mean[nb_gen-1],2), fontsize = 15, color='darkblue', ha='right')
    plt.legend(loc='best')
    return fig