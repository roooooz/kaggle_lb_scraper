'''
author: wwt117
date: 2021-1-11
reference: https://zhuanlan.zhihu.com/p/93052754
'''


import urllib3  # pip install -i https://pypi.anaconda.org/pypi/simple urllib3
import pandas as pd
import json


def data_scraper(lb_type, competition):
    url = ''
    if lb_type == 'public':
        url = 'https://www.kaggle.com/c/{competition}/leaderboard.json?includeBeforeUser=true&includeAfterUser=true'.format(
            competition=competition)
    elif lb_type == 'private':
        url = 'https://www.kaggle.com/c/{competition}/leaderboard.json?includeBeforeUser=true&includeAfterUser=true&type=private'.format(
            competition=competition)
    else:
        print('The input is error.')

    return url


def data_save(data, lb_type, competition):
    data.to_csv('{competition}_{lb_type}_rank_data.csv'.
                format(competition=competition.replace('-', '_'), lb_type=lb_type), index=False)
    print('save {competition}_{lb_type}_rank_data.csv'.
          format(competition=competition.replace('-', '_'), lb_type=lb_type))


def data_clean(data):
    pass


def data_parser(lb_type, competition):

    http = urllib3.PoolManager()
    url = data_scraper(lb_type, competition)
    response = http.request('GET', url)

    html = str(response.data, 'utf-8')

    ranks0 = str(html).replace("\\", "")
    ranks1 = json.loads(ranks0)['beforeUser']
    ranks2 = json.loads(ranks0)['afterUser']

    ranks = ranks1 + ranks2

    team_list = list(ranks)

    rank_score = pd.DataFrame(columns=['rank', 'teamName', 'score'])

    for team in team_list:
        rank = team.get('rank')
        teamName = team.get('teamName')
        score = team.get('score')
        if teamName.startswith("020") or teamName.startswith("019") or teamName.startswith("017"):
            rank_score = rank_score.append(
                {'rank': rank, 'teamName': teamName, 'score': score},
                ignore_index=True)

    print(rank_score)
    return rank_score



def main():
    competition = 'statlearning-sjtu-2020'

    # save public rank to public.csv
    pb_data = data_parser("public", competition)
    data_save(pb_data, "public", competition)


    # save private rank to private.csv
    pr_data = data_parser("private", competition)
    data_save(pr_data, "private", competition)

if __name__ == '__main__':
    main()