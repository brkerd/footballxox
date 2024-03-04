import random
import sqlite3
import pycountry

con = sqlite3.connect("tikitakapi.db", check_same_thread=False)
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

    if(len(nations)<3):
        nations, clubs = finalGrid(LeagueId)

    
    return random.sample(list(nations),3), clubs

def playerGuess(playerName, gridNat, gridClub):
    query = "SELECT DISTINCT name FROM players WHERE name LIKE ? AND country_of_citizenship LIKE ? AND current_club_name LIKE ?"
    params = (playerName, gridNat, gridClub)
    askDB = cur.execute(query, params)
    checkGuess = askDB.fetchone()

    if(checkGuess is None):
        return False
    elif(checkGuess[0] == playerName):
        return True
    else:
        return False


def getISOCode(name):
    try:
        
        # Try looking up as a subdivision
        code = pycountry.subdivisions.lookup(name).code
        if(name=="England"):
            return "GB"
        
        return code
    except LookupError:
        try:
            # If it's not a subdivision, try looking up as a country
            if(name == "Turkey"):
                name = "Türkiye"
            code = pycountry.countries.lookup(name).alpha_2
            return code
        except LookupError:
            try:
                code = pycountry.countries.search_fuzzy(name)
                return code
            except LookupError:
                print(f"Could not find flag for {name}")
                return None  