from google.appengine.ext import db
import tree
import player
import pay_code


def set_groups():
    players = player.get_all_players()
    x = 1
    for p in players:
        p.set_group_nbr(x)
        x += 1
        p.put()
        if x == 5:
            x = 1


def run_test1():
    #test ---
    pay = pay_code.Paycode(pay_code="a")
    pay.put()
    for k in range(0, 16):
        p = player.Player(nick=str(k), char_code=str(k))
        p.put()
    #test ---


def run_test2():
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
    winner_bracket_keys = [None]*15
    loser_bracket_keys = [None]*29
    i = 0
    for g in group_stage_groups:
        winner_bracket_keys[15-i] = g[0].key()
        if i < 4:
            winner_bracket_keys[15-i-5] = g[1].key()
        elif i == 4:
            winner_bracket_keys[14] = g[1].key()
        else:
            winner_bracket_keys[12] = g[1].key()
        i += 2
    i = 0
    for g in group_stage_groups:
        loser_bracket_keys[29-i] = g[2].key()
        if i < 2:
            loser_bracket_keys[29-i-5] = g[3].key()
        elif i == 2:
            loser_bracket_keys[28] = g[3].key()
        else:
            loser_bracket_keys[26] = g[3].key()
        i += 2
    tournament_table = tree.TournamentBrackets()
    tournament_table.winner_bracket = winner_bracket_keys
    tournament_table.loser_bracket = loser_bracket_keys
    tournament_table.put()





