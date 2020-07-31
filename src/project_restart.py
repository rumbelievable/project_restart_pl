import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import re 
from PlayerClass import Player

plt.style.use('ggplot')

def clean_names(df):
    names = df['name']
    names = names.apply(lambda x: re.sub(r'\d+$', '', x.replace('_', ' ')).strip())  
    df['name'] = names
    return df

def plot_player_stats(player_names, pre_df, post_df, filename):
    fig, ax = plt.subplots(2,1,figsize=(15,12))
    width=.35
    total_games_pre = len(pre_df['GW'].unique())
    total_games_post = len(post_df['GW'].unique())
    pre_goals = [pre_df[pre_df['name']==name]['goals_scored'].sum()/total_games_pre for name in player_names]
    post_goals = [post_df[post_df['name']==name]['goals_scored'].sum()/total_games_post for name in player_names]
    pre_assists = [pre_df[pre_df['name']==name]['assists'].sum()/total_games_pre for name in player_names]
    post_assists = [post_df[post_df['name']==name]['assists'].sum()/total_games_post for name in player_names]
    xlocs = np.arange(len(pre_goals))

    for i, name in enumerate(player_names):
        ax[0].plot(gw, df[df['name']==name]['goals_scored'], label=player_names[i], marker='o', linestyle=':')
    ax[0].vlines(30, 0, 3, linestyle='--', label='Project Restart')
    ax[0].legend(fontsize=15)
    ax[0].set_title('Goals per Gameweek', fontsize=22)
    ax[0].set_xlabel('Gameweek', fontsize=18)
    ax[0].set_ylabel('Number of Goals',fontsize=20)
    ax[0].set_xticks(np.arange(1,39,2))
    ax[0].set_yticks(range(4))
    ax[0].tick_params(labelsize=20)

    ax[1].bar(xlocs- width/2, post_goals, width, label='Post-Shutdown Goals', color='darkred',alpha=.75)
    ax[1].bar(xlocs- width/2, pre_goals, width, label='Pre-Shutdown Goals', color='salmon',alpha=.75)
    ax[1].bar(xlocs+ width/2, post_assists, width, label='Post-Shutdown Assists', color='midnightblue',alpha=.75)
    ax[1].bar(xlocs+ width/2, pre_assists, width, label='Pre-Shutdown Assists', color='lightsteelblue',alpha=.75)

    ax[1].set_xticks(ticks=range(len(pre_goals)))
    ax[1].set_xticklabels(player_names, fontsize=18)
    ax[1].legend(fontsize=15)
    ax[1].set_title('Total Goals Scored, Pre/Post-Shutdown', fontsize=22)
    ax[1].set_xlabel('Player', fontsize=18)
    ax[1].set_ylabel('Amount per Game', fontsize=20)

    ax[1].tick_params(labelsize=20)
    plt.tight_layout(pad=1)
    plt.savefig(f'{filename}.png', dpi=100)

if __name__ == "__main__":
    o = False
    parser = argparse.ArgumentParser(description="""Insert name of player.""")
    parser.add_argument("name", help="Player name")
    # parser.add_argument("--others", help="Other players")
    args = parser.parse_args()

    df = pd.read_csv('./data/merged_gw.csv')
    df = clean_names(df)
    pre = df[df['GW'] < 30]
    post = df[df['GW'] >= 30]

    mu_names = ['Anthony Martial', 'Mason Greenwood', 'Marcus Rashford']
    colors = ['firebrick', 'steelblue', 'forestgreen']
    df['GW'].unique()
    gw=np.arange(1,34,1)

    p = args.name
    # others = args.others

    player = Player(p, df)  
    if o:
        others = ['Anthony Martial', 'Marcus Rashford']
        player.improved_since_restart(df, others, plot=True) 
    player.improved_since_restart(df, plot=True)



    