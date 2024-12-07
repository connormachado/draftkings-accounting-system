from nba_api.stats.static import teams

# Get all NBA teams
nba_teams = teams.get_teams()

# Extract team IDs and names into a list
team_ids = [(team['id'], team['full_name']) for team in nba_teams]

# Print team IDs and names
for team_id, team_name in team_ids:
    print(f"{team_name}: {team_id}")
