from google.appengine.ext import db
import tree
import player
import group


def create_groups():
    players = player.get_all_players()
    groups = []
    for x in range(1, 4):
        groups.add(group.Group(name='Group %s' % x))
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
    tournament_table = tree.TournamentBrackets()
    winner_bracket = []
    loser_bracket = []
    while len(winner_bracket) < 7:
        winner_bracket.add(group.Group())
    q = db.GlQuery("SELECT * FROM Group")
    groups = q.get()
    for group in groups:
        sorted_list = sorted(group.list_of_players, key=lambda player: player.matches_won, reverse=True)
        for x in range(0, 1):
            tournament_table