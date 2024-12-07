from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

# All team id's
team_ids = [1610612737, 1610612738, 1610612739, 1610612740, 1610612741, 1610612742, 1610612743, 1610612744, 1610612745, 1610612746, 1610612747, 1610612748, 1610612749, 1610612750, 1610612751, 1610612752, 1610612753, 1610612754, 1610612755, 1610612756, 1610612757, 1610612758, 1610612759, 1610612760, 1610612761, 1610612762, 1610612763, 1610612764, 1610612765, 1610612766]

# Initialize an empty DataFrame to store all games
all_games = pd.DataFrame()

# Loop through each team ID and fetch game logs
for team_id in team_ids:
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    team_games = gamefinder.get_data_frames()[0]
    all_games = pd.concat([all_games, team_games], ignore_index=True)

# Save to a CSV file for future use
all_games.to_csv('all_nba_games.csv', index=False)

print("Data collection complete!")