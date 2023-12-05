import random
import sqlite3

con = sqlite3.connect("tikitakapi.db")
cur = con.cursor()

def getClubsFromCompetitionId(Id):
    query = 'SELECT DISTINCT current_club_name FROM players WHERE last_season = 2023 AND current_club_domestic_competition_id LIKE ?'
    params = (Id,)

    getClubs = cur.execute(query,params)
    
    teams = [team[0] for team in getClubs.fetchall()]
    return teams

def gridClubs(Id):
    teams = getClubsFromCompetitionId(Id)
    selectedRandom = random.sample(teams,3)
    
    return selectedRandom

def finalGrid(LeagueId):
    query = 'SELECT DISTINCT country_of_citizenship FROM players WHERE last_season = 2023 AND current_club_name LIKE ?'
    clubs = gridClubs(LeagueId)
    
    nationsForClubs = []
    for club in clubs:
        params = (club,)
        getNations = cur.execute(query,params)
        toAdd = [nation[0] for nation in getNations.fetchall()]
        nationsForClubs.append(toAdd)
        
    nations = set(nationsForClubs[0]).intersection(*nationsForClubs[1:])

    #nations = [nation for nation in nationsForClubs[0] if nation in nationsForClubs[1] and nation in nationsForClubs[2]]
    if(len(nations)<3):
        nations, clubs = finalGrid(LeagueId)

    
    return random.sample(list(nations),3), clubs

gridAllNations, gridFinalClubs = finalGrid("GB1")
print(gridFinalClubs)
print(gridAllNations)