#!/usr/bin/python3
import re
import requests
from bs4 import BeautifulSoup

def get_nba_scores():
    url = "https://sports.yahoo.com/nba/scoreboard/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        games = soup.find_all('div', class_="D(tb) W(100%) Pos(r)")
        print("----")
        for g in games:
            status = g.find_all('div', class_="Pb(4px) D(f) Jc(sb) Ai(b) Gp(4px)")
            spans = status[0].find_all('span')
            state = spans[-1].text
            
            # Find the elements containing team names and scores
            team_elements = g.select('span[data-tst="last-name"]')
            score_elements = g.select('span.YahooSans.Fw\(700\)\!.Va\(m\).Fz\(24px\)\!')

            # Extract team names and scores
            teams = [team.text.strip() for team in team_elements]
            scores = [score.text.strip() for score in score_elements]

            # Print the results
            game = []
            for team, score in zip(teams, scores):
                if len(game) == 1:
                    if abs(int(score)-int(game[0][1])) < 4:
                        print(f"\033[92m{game[0][0]} ###:### {team}\033[00m ({state})")
                    else:
                        print(f"{game[0][0]} {game[0][1]}:{score} {team} ({state})")
                    print("----")
                    game = []
                else:
                    game.append([team, score])

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    get_nba_scores()

