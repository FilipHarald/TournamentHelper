from google.appengine.ext import db
import tree
import player
import match


def create_groups():
    players = player.get_all_players()
    groups = []
    for x in range(1, 4):
        groups.append(match.Match(name='Group %s' % x))
    x = 0
    for p in players:
        groups[x].add(p)
        if not 3:
            x += 1
        else:
            x = 0
    for g in groups:
        g.put()


def run_test():
        #test ---
    win = 0
    counter = 1
    for k in range(0, 16):
        p = player.Player(nick=str(k), char_code=str(k), matches_won=win, group_nbr=counter)
        p.put()
        win += 1
        if win == 4:
            win = 0
            counter += 1
    #test ---


def set_up_tournament_table():
    group_stage_groups = [[], [], [], []]
    q = db.GqlQuery("SELECT * FROM Player ORDER BY group_nbr ASC , matches_won DESC")
    the_list = q.run()
    for p in the_list:
        group_stage_groups[p.group_nbr-1].append(p.key())
    winner_bracket = []
    loser_bracket = []
    while len(winner_bracket) < 7:
        winner_bracket.append(match.Match())
    while len(loser_bracket) < 14:
        loser_bracket.append(match.Match())
    i = 0
    for g in group_stage_groups:
        winner_bracket[6-i].add_player_key(g[0])
        if i < 2:
            winner_bracket[6-i-2].add_player_key(g[1])
        elif i == 2:
            winner_bracket[6].add_player_key(g[1])
        else:
            winner_bracket[6-2].add_player_key(g[1])
        i += 1
    i = 0
    for g in group_stage_groups:
        loser_bracket[13-i].add_player_key(g[2])
        if i < 2:
            loser_bracket[13-i-2].add_player_key(g[3])
        elif i == 2:
            loser_bracket[13].add_player_key(g[3])
        else:
            loser_bracket[13-2].add_player_key(g[3])
        i += 1
    winner_bracket_keys = []
    loser_bracket_keys = []
    for p in winner_bracket:
        p.put()
        winner_bracket_keys.append(p.key())
    for p in loser_bracket:
        p.put()
        loser_bracket_keys.append(p.key())
    tournament_table = tree.TournamentBrackets()
    tournament_table.winner_bracket = winner_bracket_keys
    tournament_table.loser_bracket = loser_bracket_keys
    tournament_table.put()





