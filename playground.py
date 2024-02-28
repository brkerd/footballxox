import random
import sqlite3
import pycountry

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
    
def toISOCode(unofficialName):
    pass



# def get_flag_url(name):
#     try:
#         # Try looking up as a subdivision
#         code = pycountry.subdivisions.lookup(name).code.lower()
#         return f"https://github.com/hampusborgos/country-flags/blob/main/svg/{code}.svg"
#     except LookupError:
#         try:
#             # If it's not a subdivision, try looking up as a country
#             country = pycountry.countries.lookup(name)
#             return country.code
#         except LookupError:
#             print(f"Could not find flag for {name}")
#             return None


# def getCode(name):
#     try:
#         # Try looking up as a subdivision
#         code = pycountry.subdivisions.lookup(name).code
#         return code
#     except LookupError:
#         try:
#             # If it's not a subdivision, try looking up as a country
#             if(name == "Turkey"):
#                 name = "Türkiye"
#             code = pycountry.countries.lookup(name).alpha_2
#             return code
#         except LookupError:
#             try:
#                 code = pycountry.countries.search_fuzzy(name)
#                 return code
#             except LookupError:
#                 print(f"Could not find flag for {name}")
#                 return None


# code = pycountry.countries.search_fuzzy("Turkey")
# print(code)

print(pycountry.subdivisions.lookup("Wales").code)

# code1 = getCode("England")
# code2 = getCode("Turkey")
# print(f"{code1}   {code2}")

# eng = pycountry.countries.lookup("Germany").alpha_2
# print(eng)



# gridAllNations, gridFinalClubs = finalGrid("GB1")

# print(gridFinalClubs)
# print(gridAllNations)
# guess = input("Guess player name: ")
# guessResult = playerGuess(guess,gridAllNations[0],gridFinalClubs[0])

# if(guessResult is True):
#     print("Correct guess!")

# if(guessResult is False):
#     print("Wrong Guess!")