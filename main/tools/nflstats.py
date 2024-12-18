import json

import nfl_data_py as nfl

import tools.utils as utils
import globals
stats = nfl.import_weekly_data([2024])

def get_nfl_stats(player_name: str, num_games=4) -> str:
    """
    Gets the stats for the last n games of a player

    Args:
        player_name (str): The name of the player
        num_games (int): The number of games to get stats for

    Returns:
        str: The stats for the player
    """
    print(player_name)
    player_name = utils.convert_player_name(player_name)
    num_games = int(num_games)

    player_stats = stats[stats["player_display_name"] == player_name]

    if player_stats.empty:
        return player_name + " not found"

    first_n_rows = player_stats.to_dict(orient='records')
    first_n_rows.reverse()
    first_n_rows = first_n_rows[:num_games]
    scoring_type = globals.get_scoring_type()
    keys_to_keep = ['recent_team', 'position', 'week', 'opponent_team', 'fantasy_points', 'passing_yards', 'passing_tds', 'interceptions', 'rushing_yards', 'rushing_tds', 'receptions', 'receiving_yards', 'receiving_tds', 'fantasy_points_ppr']

    if scoring_type == 0.5 or scoring_type == 0:
        keys_to_keep.remove('fantasy_points_ppr')
    else:
        keys_to_keep.remove('fantasy_points')

    stats_string = '\n'
    stats_string += f'---------- Recent Stats for {player_name} ----------\n'
    for elem in first_n_rows:
        elem = {k: elem[k] for k in keys_to_keep}
        # remove keys that are equal to 0 or None
        keys_to_remove = [k for k, v in elem.items() if v == 0 or v is None]

        for key in keys_to_remove:
            if elem["position"] == "QB" and key in ["passing_yards", "passing_tds", "interceptions"]:
                continue
            if elem["position"] == "RB" and key in ["rushing_yards", "rushing_tds"]:
                continue
            if elem["position"] == "WR" and key in ["receiving_yards", "receiving_tds"]:
                continue
            if elem["position"] == "TE" and key in ["receiving_yards", "receiving_tds"]:
                continue
            elem.pop(key, None)
        stats_string += json.dumps(elem)
        stats_string += '\n'
    stats_string += '-----------------------------------------------\n'
    return stats_string


get_nfl_stats_tool = {
    'type': 'function',
    'function': {
        'name': 'get_nfl_stats',
        'description': 'Get the stats for a player',
        'parameters': {
            'type': 'object',
            'required': ['player_name', 'num_games'],
            'properties': {
                'player_name': {'type': 'string', 'description': 'The name of the player'},
                'num_games': {'type': 'integer', 'description': 'The number of games to get stats for'}
            },
        },
    },
}