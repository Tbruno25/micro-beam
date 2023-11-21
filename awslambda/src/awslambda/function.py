import json
from dataclasses import dataclass, asdict
from typing import Optional

from datetime import datetime, timezone, timedelta
from typing import Optional
from nba_api.stats.static import teams

from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore


kings_id: Optional[str] = None
game_id: Optional[str] = None
start_time: Optional[str] = None
kings_team_key: Optional[str] = None
opponent_team_key: Optional[str] = None


@dataclass
class Response:
    lightBeam: bool
    sleepMinutes: int


kings = teams.find_teams_by_city("sacramento")[0]
kings_id = kings["id"]

board = scoreboard.ScoreBoard()
todays_games = board.games.get_dict()

for game in todays_games:
    if kings_id == game["awayTeam"]["teamId"]:
        kings_team_key = "awayTeam"
        opponent_team_key = "homeTeam"

    elif kings_id == game["homeTeam"]["teamId"]:
        kings_team_key = "homeTeam"
        opponent_team_key = "awayTeam"

    if kings_team_key:
        game_id = game["gameId"]
        start_time = game["gameTimeUTC"]
        break


def lambda_handler(event, context):
    response = Response(lightBeam=False, sleepMinutes=12 * 60)

    if game_id:
        game_time = datetime.fromisoformat(start_time).astimezone(timezone.utc)
        # Average NBA game duration is 2 hours 15 minutes
        # Add 2 hours to try and awaken during 4th quarter
        est_time = game_time + timedelta(hours=2)
        current_time = datetime.now(timezone.utc)
        delta_seconds = (est_time - current_time).total_seconds()
        minutes_until = max(0, delta_seconds / 60)

        if minutes_until > 0:
            response.sleepMinutes = minutes_until

        else:
            # Game should be in Q4
            box = boxscore.BoxScore(game_id)
            game = box.game.get_dict()

            if game["gameStatus"] == 3:  # Game over
                kings_win = (
                    game[kings_team_key]["score"] > game[opponent_team_key]["score"]
                )
                response.lightBeam = kings_win
            else:
                response.sleepMinutes = 2

    return json.dumps(asdict(response))
