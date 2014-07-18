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


def set_up_tournament_table



