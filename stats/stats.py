import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import imageio
import os
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
    if length > 1:
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

def generate_board_fig(board, step, player, action, scores, pool, game, players):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 14), gridspec_kw={'height_ratios': [2, 1]})
    fig.suptitle(f"Pool {pool} | Game {game}", fontsize=16)
    mask = np.array([ [ True,  True,  False, False,  True,  True,  True,  True,  True],
                        [ True,  False, False,  False, False,  True,  True,  True,  True],
                        [ True, False,  False, False,  False, False,  False,  True,  True],
                        [ True,  False, False,  False, False,  False, False,  False, False],
                        [ False, False,  False, False,  True, False,  False, False,  False],
                        [False,  False, False,  False, False,  False, False,  False,  True],
                        [ True,  True,  False, False,  False, False,  False, False,  True],
                        [ True,  True,  True,  True, False,  False, False,  False,  True],
                        [ True,  True,  True,  True,  True, False,  False,  True,  True] ])

    sns.heatmap(board.m, annot=True, cmap='coolwarm', cbar=False, linewidths=1, linecolor='black', square=True, mask=mask, vmin=-5, vmax=5, ax=ax1, annot_kws={"size": 20})
    step_to_display = f" {step}" if step < 10 else f"{step}"
    player_to_display = f" {player}" if player == 1 else f"{player}"
    ax1.set_title(f"Step {step_to_display} | Player {player_to_display} | Action {action}")
    ax1.arrow(y=action[0]+.5, x=action[1]+.5, dy=action[2]-action[0], dx=action[3]-action[1], color='red' if player==1 else 'blue', head_width=.4, head_length=.4, length_includes_head=True)
    for x in range(mask.shape[0]):
        for y in range(mask.shape[1]):
            if board.get_tower_actions_len(x, y) <= 0 and board.m[x][y] != 0:
                color = 'red' if board.m[x][y] > 0 else 'blue'
                circle = plt.Circle((y+.5, x+.5), .4, color=color, fill=False, linewidth=2)
                ax1.add_patch(circle)
    
    xs = range(len(scores))
    positive = [True if x > 0 else False for x in scores]
    negative = [False if x > 0 else True for x in scores]
    sns.lineplot(x=xs, y=scores, ax=ax2, marker='o', color='grey', linewidth=1)
    ax2.fill_between(xs, scores, where=positive, interpolate=True, color='red')
    ax2.fill_between(xs, scores, where=negative, interpolate=True, color='blue')
    rect_p1=mpatches.Rectangle((0,0),40,20, alpha=0.1,facecolor="red")
    rect_m1=mpatches.Rectangle((0,-20),40,20, alpha=0.1,facecolor="blue")
    plt.gca().add_patch(rect_p1)
    plt.gca().add_patch(rect_m1)
    ax2.set_xlim((0,40))
    ax2.set_ylim((-20,20))
    ax2.set_title('Score evolution')
    ax2.set_xticks(range(40))
    ax2.set_xticklabels(range(40), rotation=90)
    ax2.set_yticks(np.arange(-20, 22, 2))
    ax2.set_xlabel('Step')
    ax2.set_ylabel('Score')
    ax2.text(step+0.4, scores[-1]+0.2, f"{scores[-1]}", fontsize = 14, color='black', ha='center')
    ax2.add_line(plt.axhline(y=0, color='grey', linestyle='--'))
    ax2.add_line(plt.axvline(x=step, color='grey', linestyle='--'))
    ax2.text(39, 19, str(players[0]), color='red', ha="right", va="top", fontsize=14)
    ax2.text(39, -19, str(players[1]), color='blue', ha="right", va="bottom", fontsize=14)
    return fig

def generate_board_history_fig(board, history, players, path='', pool_id=0, game_id=0):
    filenames = []
    scores = [0]
    player = 1
    for i, action in enumerate(history):
        board.play_action(action)
        scores.append(board.get_score())
        fig = generate_board_fig(board, i+1, player, action, scores, pool_id, game_id, players)
        filename = f"{path}gif/board_history_{i}_{pool_id}_{game_id}.png"
        plt.savefig(filename, fig=fig)
        player = -player
        filenames.append(filename)
        plt.clf()
        plt.close()

    with imageio.get_writer(f"{path}gif/game_history_p{pool_id}_g{game_id}.gif", mode='I', fps=1) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    # Remove files
    for filename in set(filenames):
        os.remove(filename)

if __name__ == '__main__':
    generate_summary_file()
   