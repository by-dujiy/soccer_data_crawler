from app.crawler import ScrapingBot
from app.db import add_match
from app.db.db import Model, engine


LEAGUES_ARCHIVE = {
    "premier-league": "football/england/premier-league/archive/",
    "ligue-1": "football/france/ligue-1/archive/",
    "bundesliga": "football/germany/bundesliga/archive/",
    "serie_a": "football/italy/serie-a/archive/",
    "eredivisie": "football/netherlands/eredivisie/archive/",
    "laliga": "football/spain/laliga/archive/",
    "ukr-premier-league": "football/ukraine/premier-league/archive/"
}

sb = ScrapingBot(3, 30)

if __name__ == '__main__':
    Model.metadata.create_all(engine)
    # Model.metadata.drop_all(engine)
    urls = sb.parse_league_page("football/england/premier-league-2023-2024/results/")
    for event_url in urls:
        match_data = sb.parse_match(event_url)
        if match_data:
            add_match(match_data)

    sb.quit()
