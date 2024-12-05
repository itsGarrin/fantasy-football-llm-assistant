from sleeper_wrapper import Stats, Players

player_data = Players().get_all_players()
season_type = "regular"


def get_player_projected_points(player_name, season, week, scoring_format="ppr"):
    """
    Retrieve the projected fantasy points for a specific player for the given match week.

    Parameters:
    ----------
    player_name : str
        The full name of the player (case insensitive).
    season : int
        The season year (e.g., 2024).
    week : int
        The week number for which to retrieve projections (e.g., 1-17 for regular season).
    scoring_format : str, optional
        The scoring format for projections (default is "ppr"). Options include:
        - "ppr" for points per reception
        - "half_ppr" for half points per reception
        - "standard" for no points per reception

    Returns:
    -------
    float
        The projected fantasy points for the player in the specified week and scoring format.
    str
        If the player's name is not found in the dataset, a descriptive error message is returned.

    Notes:
    ------
    - The function uses Sleeper API data to retrieve player projections.
    - Player projections are derived based on the season type ("regular").
    - Ensure the player data is up to date to prevent missing or incorrect projections.

    Examples:
    ---------
    >>> get_player_projected_points("Christian McCaffrey", 2024, 8)
    22.5
    >>> get_player_projected_points("Nonexistent Player", 2024, 8)
    "Player 'Nonexistent Player' not found."
    """
    stats = Stats()
    week_projections = stats.get_week_projections(season_type, season, week)

    # Find player ID from the name
    player_id = next(
        (pid for pid, pdata in player_data.items() if pdata.get("full_name").lower() == player_name.lower()), None)

    if not player_id:
        return f"Player '{player_name}' not found."

    projected_points = week_projections.get(str(player_id), {}).get(f"pts_{scoring_format}", 0)
    return projected_points

def get_player_total_projected_points(player_name, season, current_week, total_weeks=17, scoring_format="ppr"):
    """
    Calculate the total projected fantasy points for a specific player for the rest of the season.

    Parameters:
    ----------
    player_name : str
        The full name of the player (case insensitive).
    season : int
        The season year (e.g., 2024).
    current_week : int
        The current week number (e.g., 8). The calculation starts from this week onward.
    total_weeks : int, optional
        The total number of weeks in the season (default is 17). Adjust for custom leagues.
    scoring_format : str, optional
        The scoring format for projections (default is "ppr"). Options include:
        - "ppr" for points per reception
        - "half_ppr" for half points per reception
        - "standard" for no points per reception

    Returns:
    -------
    float
        The total projected fantasy points for the player for the rest of the season in the specified scoring format.
    str
        If the player's name is not found in the dataset, a descriptive error message is returned.

    Notes:
    ------
    - The function aggregates weekly projections from the current week to the end of the season.
    - Player projections are based on the Sleeper API's data for the "regular" season.
    - Use this function to evaluate long-term potential when making trades or waiver wire decisions.

    Examples:
    ---------
    >>> get_player_total_projected_points("Justin Jefferson", 2024, 8)
    105.3
    >>> get_player_total_projected_points("Nonexistent Player", 2024, 8)
    "Player 'Nonexistent Player' not found."
    """
    stats = Stats()
    total_projected_points = 0

    # Find player ID from the name
    player_id = next(
        (pid for pid, pdata in player_data.items() if pdata.get("full_name").lower() == player_name.lower()), None)

    if not player_id:
        return f"Player '{player_name}' not found."

    for week in range(current_week, total_weeks + 1):
        week_projections = stats.get_week_projections(season_type, season, week)
        total_projected_points += week_projections.get(str(player_id), {}).get(f"pts_{scoring_format}", 0)

    return total_projected_points



get_player_projected_points_tool = {
    'type': 'function',
    'function': {
        'name': 'get_player_projected_points',
        'description': 'Get the projected points for a player',
        'parameters': {
            'type': 'object',
            'required': ['player_name', 'season_type', 'season', 'week'],
            'properties': {
                'player_name': {'type': 'string', 'description': 'The name of the player'},
                'season': {'type': 'integer', 'description': 'The season year'},
                'week': {'type': 'integer', 'description': 'The week number'},
                'scoring_format': {'type': 'string', 'description': 'The scoring format'},
            },
        },
    },
}

get_player_total_projected_points_tool = {
    'type': 'function',
    'function': {
        'name': 'get_player_total_projected_points',
        'description': 'Get the total projected points for a player',
        'parameters': {
            'type': 'object',
            'required': ['player_name', 'season_type', 'season', 'current_week', 'total_weeks'],
            'properties': {
                'player_name': {'type': 'string', 'description': 'The name of the player'},
                'season': {'type': 'integer', 'description': 'The season year'},
                'current_week': {'type': 'integer', 'description': 'The current week'},
                'total_weeks': {'type': 'integer', 'description': 'The total number of weeks'},
                'scoring_format': {'type': 'string', 'description': 'The scoring format'},
            },
        },
    },
}