from google.appengine.ext import db
import tree
import player
import group

def create_groups():
    players = player.get_all_players()
    groups = []
    for x in range(1, 4):
        groups.__add__(group.Group(name='Group %s' % x))
    x = 0
    for p in players:
        groups[x].add(p)
        if not 3:
            x += 1
        else:
            x = 0
    for g in groups:
        g.put()


def set_up_tournament_table():
    #test ---
    g = group.Group(name='first')
    win = 0
    for k in (0, 16):
        p = player.Player(nick=k, char_code=k, matches_won=win)
        win += 1
        if win == 4:
            win = 0
        p.put()
        g.add_test_player(p)
        if not win == 0 and (win % 4 == 0):
            g.put
            g = group.Group(name=k)
    #test ---
    tournament_table = tree.TournamentBrackets()
    winner_bracket = []
    loser_bracket = []
    groupstage_groups = db.GlQuery("SELECT * FROM Group").get()
    while len(winner_bracket) < 7:
        winner_bracket.__add__(group.Group())
    while len(loser_bracket) < 14:
        loser_bracket.__add__(group.Group())
    i = 0
    for g in groupstage_groups:
        sorted_list = sorted(g.list_of_players, key=lambda player: player.matches_won, reverse=True)
        winner_bracket[6-i].add_player(sorted_list[0])
        if i < 2:
            winner_bracket[6-i-2].add_player(sorted_list[1])
        elif i == 2:
            winner_bracket[6].add_player(sorted_list[1])
        else:
            winner_bracket[6-2].add_player(sorted_list[1])
        i += 1
    i = 0
    for g in groupstage_groups:
        sorted_list = sorted(g.list_of_players, key=lambda player: player.matches_won)
        loser_bracket[13-i].add_player(sorted_list[0])
        if i < 2:
            loser_bracket[13-i-2].add_player(sorted_list[1])
        elif i == 2:
            loser_bracket[13].add_player(sorted_list[1])
        else:
            loser_bracket[13-2].add_player(sorted_list[1])
        i += 1
    tournament_table.winner_bracket = winner_bracket
    tournament_table.loser_bracket = loser_bracket
    tournament_table.put()





