from fastapi import APIRouter
from functions import finalGrid, playerGuess, getISOCode

router = APIRouter()

@router.get("/final_grid/{league_id}")
def final_grid(league_id: str):
    nations, clubs = finalGrid(league_id)
    return{"nations":nations, "clubs":clubs}

@router.get("/guess_player/{player_name}/{nationality}/{club}")
def guess_player(player_name: str, nationality: str, club: str):
    answer = playerGuess(player_name,nationality,club)
    return answer


@router.get("/club_logo/{league_id}/{club_name}")
def club_logo(league_id: str, club_name: str):
    logoURL = f"https://raw.githubusercontent.com/luukhopman/football-logos/master/logos/{league_id}/{club_name}.png"
    return{"logoURL": logoURL}

@router.get("/country_iso/{country_name}")
def get_ISO_code(country_name: str):
    code = getISOCode(country_name)
    return{"countryISO":code}
