from collections import defaultdict
import random
import time
import csv
import pprint
import math

def generate_random_schedule(players):
    n_players = len(players) - 1
    schedule = {}
    for i in player_ids:
        reader = players[i]
        match_players = [player for pid, player in players.items() if pid != i]
        random.shuffle(match_players)
        schedule[reader] = [match_players[:math.ceil(n_players/2)], match_players[math.ceil(n_players/2):]]
    return schedule


def find_schedule_cost(schedule):
    player_matrix = defaultdict(lambda: defaultdict(int))
    for match, teams in schedule.items():
        team_1 = teams[0]
        for t1 in team_1:
            for t in team_1:
                if t != t1:
                    player_matrix[t1][t] += 1
        team_2 = teams[1]
        for t2 in team_1:  # exactly same for team 2
            for t in team_2:
                if t != t2:
                    player_matrix[t2][t] += 1
    # cost is the range of values for how many times each player plays each other, so need max and min
    max_per_player = []
    min_per_player = []
    for _, p in player_matrix.items():
        max_per_player.append(max(p.values()))
        min_per_player.append(min(p.values()))
    max_games = max(max_per_player)
    min_games = min(min_per_player)
    cost = max_games - min_games
    return cost


def write_schedule_to_csv(filename, schedule):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, ['Reader',
                                    'Team 1 Player 1',
                                    'Team 1 Player 2',
                                    'Team 1 Player 3',
                                    'Team 1 Player 4',
                                    'Team 2 Player 1',
                                    'Team 2 Player 2',
                                    'Team 2 Player 3',
                                    'Team 2 Player 4'])
        writer.writeheader()
        for k, v in schedule.items():
            writeable_row = {}
            writeable_row['Reader'] = k
            writeable_row['Team 1 Player 1'] = v[0][0]
            writeable_row['Team 1 Player 2'] = v[0][1]
            writeable_row['Team 1 Player 3'] = v[0][2]
            writeable_row['Team 1 Player 4'] = v[0][3]
            writeable_row['Team 2 Player 1'] = v[1][0]
            writeable_row['Team 2 Player 2'] = v[1][1]
            writeable_row['Team 2 Player 3'] = v[1][2]
            writeable_row['Team 2 Player 4'] = v[1][3]
            writer.writerow(writeable_row)


if __name__ == '__main__':
    """
    NOTE that while the scheduler will put you in two teams, this really only properly works at the moment
    for 9 people ie. one reader and two groups of four. With a bit more work you could extend this to an
    infinite number of group, but ideally your tournament size has to be of player 4n+1 where n is an integer >= 0
    anyway. The cost function would have to be generalised to more than 2 teams and the csv writer also adapted, but
    shouldn't be that difficult. Also no work has been done on optimisation of this code, so it usually runs for a few
    mins before finding the optimum allocation. I haven't proved it, but my conjecture is that the optimum allocation 
    for n total players is (math.floor((n_players-2)/2) % 2), ie. for even players you should be able to play each other
    same number of games, and for odd number you should play each other within a range of 1.
    """
    raw_input = input('Please input comma separated names you want to make a schedule for \n')
    player_names = raw_input.split(', ')
    players = {(i+1): player_names[i] for i in range(len(player_names))}

    filename = 'schedule_{}.csv'.format(time.strftime("%Y-%m-%d", time.gmtime()))
    player_ids = players.keys()
    iterations = 10000
    schedule_cost = len(player_ids) + 1  # so always set
    start = time.time()
    optimum_schedule = None
    for i in range(iterations):
        schedule = generate_random_schedule(players)
        test_schedule_cost = find_schedule_cost(schedule)
        if test_schedule_cost < schedule_cost:
            schedule_cost = test_schedule_cost
            optimum_schedule = schedule
            if schedule_cost == 0:  # found optimum
                break
    end = time.time()
    print('Time taken to run {} iterations: {} seconds'.format(iterations, end - start))
    print('Schedule cost: {}'.format(schedule_cost))
    pprint.pprint(optimum_schedule)
    if filename:
        write_schedule_to_csv(filename=filename, schedule=optimum_schedule)

