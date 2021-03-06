import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

plt.style.use('ggplot')

def get_cumsum_pts_dict(teams):
    cumsums = {}
    points = {}
    for t in teams:
        new_df = df[(df['HomeTeam']==t) | (df['AwayTeam']==t)]
        pts = []
        for i in range(len(new_df)):
            if (new_df['HomeTeam'].iloc[i]==t) & (new_df['FTR'].iloc[i]=='H'):
                pts.append(3)
            elif (new_df['HomeTeam'].iloc[i]==t) & (new_df['FTR'].iloc[i]=='A'):
                pts.append(0)
            elif (new_df['AwayTeam'].iloc[i]==t) & (new_df['FTR'].iloc[i]=='A'):
                pts.append(3)
            elif (new_df['AwayTeam'].iloc[i]==t) & (new_df['FTR'].iloc[i]=='H'):
                pts.append(0)
            else:
                pts.append(1)
        new_df['pts']=pts
        points[t] = new_df['pts']
        cumsums[t] = new_df['pts'].cumsum()
    return points, cumsums

def get_gs_dict(teams):
    stats = {}
    for t in teams:
        new_df = df[(df['HomeTeam']==t) | (df['AwayTeam']==t)]
        s = []
        for i in range(len(new_df)):
            if new_df['HomeTeam'].iloc[i]==t:
                s.append(new_df.iloc[i]['FTHG'])
            elif new_df['AwayTeam'].iloc[i]==t:
                s.append(new_df.iloc[i]['FTAG'])
            else:
                continue
        stats[t] = s
    return stats

def plot_cumsums(cumsums):
    fig, ax = plt.subplots(1,1,figsize=(15,7))
    for i, t in enumerate(teams):
        ax.plot(range(1,39), cumsums[t], label=t, color=colors[i])
        ax.annotate(cumsums[t].values[-1], xy=(38, cumsums[t].values[-1]), fontsize=12)
    ax.set_title('Points by Team', fontsize=22)
    ax.set_xlabel('Gameweek', fontsize=19)
    ax.set_ylabel('Number of Points', fontsize=19)
    ax.set_xticks(range(1,39))
    plt.tick_params(labelsize=14)
    ax.legend()
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles, labels)
    plt.savefig('point_totals.png', dpi=100)

def plot_gs(dictionary_of_stats, teams_to_plot, save=False):
    fig, ax = plt.subplots(1,1,figsize=(15,7))
    for t in teams:
    #     ax.plot(range(1,39), gs[t], label=t, color=color_dict[t], marker='o')
        c = np.array(dictionary_of_stats[t])
        ax.plot(range(1,39), np.cumsum(c), ls='--', color=color_dict[t], alpha=.8)
        ax.annotate(f'{t}: {np.cumsum(c)[-1]}', xy=(38, np.cumsum(c)[-1]), fontsize=12)
    # ax.legend()
    # handles, labels = ax.get_legend_handles_labels()
    # labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    # ax.legend(handles, labels)
    ax.set_title('Cumulative Goals Scored - All Teams', fontsize=22)
    ax.set_xlabel('Gameweek', fontsize=19)
    ax.set_ylabel('Number of Goals Scored', fontsize=19)
    ax.vlines(30, ymin=0, ymax=100, ls='--')
    ax.annotate('Project Restart', xy=(27.5, 101), fontsize=14)
    plt.tick_params(labelsize=16)
    plt.tight_layout(pad=1)
    if save:
        plt.savefig('images/cumulative_gs.png', dpi=100)

def make_table(cumsum_dict):
    table = {t:cumsum_dict[t].iloc[-1] for t in cumsum_dict.keys()}
    table = {k: v for k, v in sorted(table.items(), key=lambda item: item[1], reverse=True)}
    return table

def make_pre_post_tables(points_dict):
    pre = {t:points[t].values[0:29].mean() for t in points.keys()}
    post = {t:points[t].values[29:].mean() for t in points.keys()}
    sorted_pre = {k:pre[k] for k,v in table.items()}
    sorted_post = {k:post[k] for k,v in table.items()}
    return sorted_pre, sorted_post

def ttest_ppg(points_dict):
    '''
    Perform a two-sample t-test on the average points per game before and after the restart for all teams.
    
    Input: teams (list): List of teams
           points_dict (dict): Dictionary of teams and points per gameweek
    Output: p_values (dict): Dictionary of teams and their resultant p-values from the t-test
    '''
    p_values = {}
    for team in points_dict.keys():
        t, p = ttest_ind(points_dict[team][0:29], points_dict[team][30:], equal_var=True)
        p_values[team]= p
    return p_values

if __name__ == '__main__':
    df = pd.read_csv('data/E0.csv')

    teams = df['HomeTeam'].unique()
    colors = ['red', 'deepskyblue', 'maroon', 'cornflowerblue', 'orangered','yellow', 'cadetblue', 'blue', 
            'mediumblue', 'firebrick', 'salmon', 'gold', 'steelblue', 'navy', 'brown', 'royalblue', 
            'darkgrey', 'darkgoldenrod', 'dodgerblue', 'crimson']
    color_dict = {x:y for x, y in zip(teams, colors)}
    sorted_color_dict = {k:color_dict[k] for k,v in table.items()}
    points, cumsums = get_cumsum_pts_dict(teams)
    table = make_table(cumsums)
    pre_covid_ppg, post_covid_ppg = make_pre_post_tables(points)

    p_vals = ttest_ppg(teams)
    for t, p in p_vals.items():
        if p <= .05:
            print(f"For a significance level of .05, {t}'s points per game average change was statistically significant with a p-value of: {round(p, 3)}.\nTheir points per game average went from {round(points[t][0:29].mean(), 3)} ppg to {round(points[t][30:].mean(), 3)} ppg.")
        if .05 <= p <= .1:
            print(f"For significance level of .1, {t}'s points per game average change was statistically significant with a p-value of: {round(p, 3)}.\nTheir points per game average went from {round(points[t][0:29].mean(), 3)} ppg to {round(points[t][30:].mean(), 3)} ppg.")