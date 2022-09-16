import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_scores_fig(df):
    length = df.shape[0]
    fig = plt.figure(figsize=(20, df.shape[0]+2))
    sns.set_theme()
    x_ticks = np.arange(-20, 22, 2)
    y_ticks = np.arange(0, length, 1)
    rect_p1=mpatches.Rectangle((0,-1),20,length+1, alpha=0.1,facecolor="red")
    rect_m1=mpatches.Rectangle((-20,-1),20,length+1, alpha=0.1,facecolor="blue")
    plt.gca().add_patch(rect_p1)
    plt.gca().add_patch(rect_m1)
    a = sns.violinplot(data=df['Scores'], palette="flare", inner="points", orient="h")
    # Tendency of the mean score
    z = np.polyfit(y_ticks, df['mean_scores'], 1)
    p = np.poly1d(z)
    plt.plot(p(y_ticks), y_ticks, c="green", ls=":", label="Tendency", linewidth=2)
    plt.xlim((-20, 20))
    plt.ylim((length, -1))
   

    a.set(title='Score distribution for each pool', xlabel='Scores', ylabel='Pool', xticks=x_ticks)
    a.set_xticklabels(x_ticks, rotation=45)
    a.text(10, -0.1, 'Player +1', fontsize = 10, color='red', ha='center')
    a.text(-10, -0.1, 'Player -1', fontsize = 10, color='blue', ha='center')
    a.add_line(plt.axvline(x=0, color='grey', linestyle='--'))

    for row in df.iterrows():
        a.text(-20, row[0]+0.2, str(row[1]['Agent -1']), color='grey', ha="left", fontsize=8)
        a.text(20, row[0]+0.2, str(row[1]['Agent 1']), color='grey', ha="right", fontsize=8)
    return fig

def generate_steps_fig(df):
    length = df.shape[0]
    fig = plt.figure(figsize=(20, df.shape[0]+2))
    sns.set_theme()
    x_ticks = np.arange(20, 48, 2)

    sns.violinplot(data=df['Steps'], palette="flare", inner="points", orient="h")
    plt.xlim((20, 46))

    plt.title('Step distribution for each pool')
    plt.xlabel('Steps')
    plt.ylabel('Pool')
    plt.xticks(x_ticks, rotation=45)
    
    return fig

def generate_win_rate_fig(df):
    fig = plt.figure(figsize=(df.shape[0]+1, 20))
    df['Cumulative_m1'] = df['Pct Agent -1'] * 100

    df['Cumulative_draw'] = df['Pct Draw']*100 + df['Pct Agent -1']*100
    df['Cumulative_p1'] = df['Cumulative_draw'] + df['Pct Agent 1']*100

    bar_p1 = sns.barplot(x=df.index, y="Cumulative_p1", data=df, color='red')
    bar_draw = sns.barplot(x=df.index, y="Cumulative_draw", data=df, color='orange')
    bar_m1 = sns.barplot(x=df.index, y="Cumulative_m1", data=df, color='blue')

    m1_bar = mpatches.Patch(color='blue', label='Agent -1')
    draw_bar = mpatches.Patch(color='orange', label='Draw')
    p1_bar = mpatches.Patch(color='red', label='Agent 1')

    for row in df.iterrows():
        if row[1]['Pct Agent -1'] != 0:
            plt.text(row[0], 1,str(row[1]['Agent -1']), color='white', ha="center", fontsize=8)
            plt.text(row[0], row[1]['Cumulative_m1']/2, str(int(row[1]['Pct Agent -1']*100))+'%', color='white', ha="center", fontsize=9)
        if row[1]['Pct Draw'] != 0:
            plt.text(row[0], row[1]['Cumulative_m1']+1, 'Draw', color='white', ha="center", fontsize=8)
            plt.text(row[0], row[1]['Cumulative_m1']+row[1]['Pct Draw']*50, str(int(row[1]['Pct Draw']*100))+'%', color='white', ha="center", fontsize=9)
        if row[1]['Pct Agent 1'] != 0:
            plt.text(row[0], row[1]['Cumulative_draw']+1,str(row[1]['Agent 1']), color='white', ha="center", fontsize=8)
            plt.text(row[0], row[1]['Cumulative_draw']+row[1]['Pct Agent 1']*50, str(int(row[1]['Pct Agent 1']*100))+'%', color='white', ha="center", fontsize=9)


    plt.ylim((0,100))
    plt.title('Pourcentage of win for each agent in each pool')
    plt.ylabel('Pourcentage')
    plt.legend(handles=[m1_bar, draw_bar, p1_bar])
    x_ticks = np.arange(0, df.shape[0]+1, 1)
    plt.xticks(x_ticks, rotation=45)
    return fig


def generate_summary_file(path=''):
    game_df = pd.read_csv(f"{path}game_results.csv", sep=';', index_col=0)
    game_df['Scores'] = game_df['Scores'].apply(lambda x: [int(a) for a in x.replace('[', '').replace(']', '').replace(' ', '').split(',')])
    game_df['Steps'] = game_df['Steps'].apply(lambda x: [int(a) for a in x.replace('[', '').replace(']', '').replace(' ', '').split(',')])
    game_df['mean_scores'] = game_df['Scores'].apply(lambda x: np.mean(x))

    pool_df = pd.read_csv(f"{path}pool_results.csv", sep=';', index_col=0)

    with PdfPages(f"{path}summary_file.pdf") as pdf:
        fig1 = generate_scores_fig(game_df)
        pdf.savefig(fig1)
        fig2 = generate_steps_fig(game_df)
        pdf.savefig(fig2)
        fig3 = generate_win_rate_fig(pool_df)
        pdf.savefig(fig3)


if __name__ == '__main__':
    generate_summary_file()
   