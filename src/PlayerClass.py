import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import ttest_ind

class Player(object):

    def __init__(self, name, df):
        # if ' '.join(df['name'].values) not in name:
        #     break
        self.name = name
        self.df = df[df['name']==self.name]
        self.pre_cv = self.df[self.df['GW'] < 30]
        self.post_cv = self.df[self.df['GW'] >=30]
        self.goals = self._get_goals()
        self.assists = self._get_assists()
        self.minutes_played = self._get_mins()
        self.yellow = self._get_yellow()
        self.red = self._get_red()
        self.stats = f'Player Stats for: {self.name}:\n Total Goals: {sum(self.goals)}\n Total Assists: {sum(self.assists)}\n Total Minutes Played: {sum(self.minutes)}\n Total Yellow Cards: {sum(self.yellow)}\n Total Red Cards: {sum(self.red)}'


    def __repr__(self):
        return self.name

    def _get_goals(self):
        self.goals = self.df['goals_scored'].values
        self.pre_goals = self.pre_cv['goals_scored'].values
        self.post_goals = self.post_cv['goals_scored'].values
        return self.goals

    def _get_assists(self):
        self.assists = self.df['assists'].values
        self.pre_assists = self.pre_cv['assists'].values
        self.post_assists = self.post_cv['assists'].values
        return self.assists

    def _get_yellow(self):
        self.yellow = self.df['yellow_cards'].values
        self.pre_yellow = self.pre_cv['yellow_cards'].values
        self.post_yellow = self.post_cv['yellow_cards'].values
        return self.yellow

    def _get_red(self):
        self.red = self.df['red_cards'].values
        self.pre_red = self.pre_cv['red_cards'].values
        self.post_red = self.post_cv['red_cards'].values
        return self.red

    def _get_mins(self):
        self.minutes = self.df['minutes'].values
        return self.minutes

    def get_weekly_goals(self):
        pass

    def _ttest(self):
        self.t_goals, self.p_goals = ttest_ind(self.pre_goals, self.post_goals, equal_var=True)
        self.t_assists, self.p_assists = ttest_ind(self.pre_assists, self.post_assists, equal_var=True)
        return [self.p_goals, self.p_assists]

    def improved_since_restart(self, df, others=None, plot=False):
        pre = df[df['GW'] < 30]
        post = df[df['GW'] >= 30]
        if plot:
            fig, ax = plt.subplots(2,1,figsize=(15,12))
            width=.35
            total_games_pre = len(self.pre_cv['GW'].unique())
            total_games_post = len(self.post_cv['GW'].unique())
            gw = np.arange(1,34,1)
            if others is not None:
                others.append(self.name)
                g = np.array([[df[df['name']==name].iloc[i]['goals_scored'] if df[df['name']==name].iloc[i]['minutes'] > 0 else None for i in range(len(df[df['name']==name]['goals_scored'].values))] for name in others])
                # pre_goals = [pre[pre['name']==name]['goals_scored'].sum()/total_games_pre for name in others]
                # post_goals = [post[post['name']==name]['goals_scored'].sum()/total_games_post for name in others]
                # pre_assists = [pre[pre['name']==name]['assists'].sum()/total_games_pre for name in others]
                # post_assists = [post[post['name']==name]['assists'].sum()/total_games_post for name in others]
                # xlocs = np.arange(g.shape[1])
                xlocs = np.arange(len(others))
                xticks = range(g.shape[0])

                for i, name in enumerate(others):
                    ax[0].plot(gw, g[i], label=others[i], marker='o', linestyle=':')
                    # ax[0].plot(gw, df[df['name']==name]['goals_scored'], label=others[i], marker='o', linestyle=':')
                ax[0].vlines(30, 0, 3, linestyle='--', label='Project Restart')
                ax[0].legend(fontsize=15)
                ax[0].set_title('Goals per Gameweek', fontsize=22)
                ax[0].set_xlabel('Gameweek', fontsize=18)
                ax[0].set_ylabel('Number of Goals',fontsize=20)
                ax[0].set_xticks(np.arange(1,39,2))
                ax[0].set_yticks(range(4))
                ax[0].tick_params(labelsize=20)

                pre_g = np.array([[pre[pre['name']==name].iloc[i]['goals_scored'] if pre[pre['name']==name].iloc[i]['minutes'] > 0 else None for i in range(len(pre[pre['name']==name]['goals_scored'].values))] for name in others])
                post_g = np.array([[post[post['name']==name].iloc[i]['goals_scored'] if post[post['name']==name].iloc[i]['minutes'] > 0 else None for i in range(len(post[post['name']==name]['goals_scored'].values))] for name in others])
                pre_a = np.array([[pre[pre['name']==name].iloc[i]['assists'] if pre[pre['name']==name].iloc[i]['minutes'] > 0 else None for i in range(len(pre[pre['name']==name]['assists'].values))] for name in others])
                post_a = np.array([[post[post['name']==name].iloc[i]['assists'] if post[post['name']==name].iloc[i]['minutes'] > 0 else None for i in range(len(post[post['name']==name]['assists'].values))] for name in others])
                pre_g = np.array(pre_g, dtype=np.float) 
                total_games_played_pre = np.sum(~np.isnan(pre_g), axis=1) 
                pre_g = np.nansum(pre_g, axis=1)  ## Counts num goals
                pre_g = pre_g/total_games_played_pre
                post_g = np.array(post_g, dtype=np.float) 
                total_games_played_post = np.sum(~np.isnan(post_g), axis=1) 
                post_g = np.nansum(post_g, axis=1)  ## Counts num goals
                post_g = post_g/total_games_played_post
                pre_a = np.array(pre_a, dtype=np.float) 
                total_games_played_pre = np.sum(~np.isnan(pre_a), axis=1) 
                pre_a = np.nansum(pre_a, axis=1)  
                pre_a = pre_a/total_games_played_pre
                post_a = np.array(post_a, dtype=np.float) 
                total_games_played_post = np.sum(~np.isnan(post_a), axis=1) 
                post_a = np.nansum(post_a, axis=1)  
                post_a = post_a/total_games_played_post
            else:
                pre_g = np.array([pre[pre['name']==self.name].iloc[i]['goals_scored'] if pre[pre['name']==self.name].iloc[i]['minutes'] > 0 else None for i in range(len(pre[pre['name']==self.name]['goals_scored'].values))])
                post_g = np.array([post[post['name']==self.name].iloc[i]['goals_scored'] if post[post['name']==self.name].iloc[i]['minutes'] > 0 else None for i in range(len(post[post['name']==self.name]['goals_scored'].values))])
                pre_a = np.array([pre[pre['name']==self.name].iloc[i]['assists'] if pre[pre['name']==self.name].iloc[i]['minutes'] > 0 else None for i in range(len(pre[pre['name']==self.name]['assists'].values))])
                post_a = np.array([post[post['name']==self.name].iloc[i]['assists'] if post[post['name']==self.name].iloc[i]['minutes'] > 0 else None for i in range(len(post[post['name']==self.name]['assists'].values))])
                # pre_goals = self.pre_cv['goals_scored'].sum()/total_games_pre
                # post_goals = self.post_cv['goals_scored'].sum()/total_games_post
                # pre_assists = self.pre_cv['assists'].sum()/total_games_pre
                # post_assists = self.post_cv['assists'].sum()/total_games_post
                xlocs = 1
                xticks = range(1)
                ax[0].plot(gw, self.df['goals_scored'], label=self.name, marker='o', linestyle=':')
                ax[0].vlines(30, 0, 3, linestyle='--', label='Project Restart')
                ax[0].legend(fontsize=15)
                ax[0].set_title('Goals per Gameweek', fontsize=22)
                ax[0].set_xlabel('Gameweek', fontsize=18)
                ax[0].set_ylabel('Number of Goals',fontsize=20)
                ax[0].set_xticks(np.arange(1,39,2))
                ax[0].set_yticks(range(4))
                ax[0].tick_params(labelsize=20)
                others = self.name

            ax[1].bar(xlocs- width/2, post_g, width, label='Post-Shutdown Goals', color='darkred',alpha=.75)
            ax[1].bar(xlocs- width/2, pre_g, width-.1, label='Pre-Shutdown Goals', color='salmon',alpha=.75)
            ax[1].bar(xlocs+ width/2, post_a, width, label='Post-Shutdown Assists', color='midnightblue',alpha=.75)
            ax[1].bar(xlocs+ width/2, pre_a, width-.1, label='Pre-Shutdown Assists', color='lightsteelblue',alpha=.75)

            ax[1].set_xticks(ticks=xticks)
            ax[1].set_xticklabels(others, fontsize=18)
            ax[1].legend(fontsize=15)
            ax[1].set_title('Total Goals Scored, Pre/Post-Shutdown', fontsize=22)
            ax[1].set_xlabel('Player', fontsize=18)
            ax[1].set_ylabel('Amount per Game', fontsize=20)

            ax[1].tick_params(labelsize=20)
            plt.tight_layout(pad=1)
            if type(others) == list:
                others = '_'.join(others)
            plt.savefig(f'{self.name}_{others}.png', dpi=100)

        p_values = self._ttest()
        messages = ['goal', 'assist']
        for i, t in enumerate(p_values):
            if t < .05:
                print(f'{self.name} has significantly improved/declined their {messages[i]} tally since the restart, with a p-value of {round(t, 3)}.')
            else:
                print(f'{self.name} has not significantly improved/declined their {messages[i]} tally since the restart, with a p-value of {round(t, 3)}.')
        