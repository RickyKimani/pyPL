# Written by Ricky Kimani
## Nov.2024

import requests
from datetime import datetime

class Fpl:
    def __init__(self, managerID: int) -> None:
        self.managerID = managerID
        if not isinstance(managerID, int) or len(str(managerID)) != 7:
            raise ValueError("Invalid manager ID. A manager ID must be a 7-digit integer.")
        
        self._url = f"https://fantasy.premierleague.com/api/entry/{managerID}/"
        self._response = requests.get(self._url)
        
        # Check for response status code
        if not self._checkStatusCode():
            raise ConnectionError(f"Failed to retrieve data. Status code: {self._response.status_code}")
        
        try:
            self._jsonResponse = self._response.json()
        except ValueError:
            raise ValueError("Invalid response format: Response is not JSON.")

    def __str__(self) -> str:
        return f"{self.name()}, {self.summary_event_points()} points"
    
    def _checkStatusCode(self) -> bool:
        status_code = self._response.status_code
        if status_code != 200:
            print("Error:", status_code)
            return False
        return True

    def id(self) -> int:
        return self._jsonResponse["id"]

    def joined_time(self) -> datetime:
        return datetime.strptime(self._jsonResponse["joined_time"], "%Y-%m-%dT%H:%M:%S.%fZ")

    def started_event(self) -> int:
        return self._jsonResponse["started_event"]

    def favorite_team(self) -> int:
        return self._jsonResponse["favorite_team"]

    def player_first_name(self) -> str:
        return self._jsonResponse["player_first_name"]

    def player_last_name(self) -> str:
        return self._jsonResponse["player_last_name"]

    def player_region_id(self) -> int:
        return self._jsonResponse["player_region_id"]

    def player_region_name(self) -> str:
        return self._jsonResponse["player_region_name"]

    def player_region_iso_code_short(self) -> str:
        return self._jsonResponse["player_region_iso_code_short"]

    def player_region_iso_code_long(self) -> str:
        return self._jsonResponse["player_region_iso_code_long"]

    def years_active(self) -> int:
        return self._jsonResponse["years_active"]

    def summary_overall_points(self) -> int:
        return self._jsonResponse["summary_overall_points"]

    def summary_overall_rank(self) -> int:
        return self._jsonResponse["summary_overall_rank"]

    def summary_event_points(self) -> int:
        return self._jsonResponse["summary_event_points"]

    def summary_event_rank(self) -> int:
        return self._jsonResponse["summary_event_rank"]

    def current_event(self) -> int:
        return self._jsonResponse["current_event"]

    def leagues(self):
        return self._jsonResponse["leagues"]

    def number_of_classic_leagues(self) -> int:
        return len(self.leagues()["classic"])

    def leagues_classic(self, n: int):
        if not isinstance(n, int) or n < 0 or n >= self.number_of_classic_leagues():
            raise ValueError(f"Error, {n} is not valid. Use a number between 0 and {self.number_of_classic_leagues() - 1}")
        return self.leagues()["classic"][n]

    def name(self) -> str:
        return self._jsonResponse["name"]

    def name_change_blocked(self) -> bool:
        return self._jsonResponse["name_change_blocked"]

    def entered_events(self) -> list:
        return self._jsonResponse["entered_events"]

    def kit(self):
        return self._jsonResponse["kit"]

    def last_deadline_bank(self) -> int:
        return self._jsonResponse["last_deadline_bank"]

    def last_deadline_value(self) -> int:
        return self._jsonResponse["last_deadline_value"]

    def last_deadline_total_transfers(self) -> int:
        return self._jsonResponse["last_deadline_total_transfers"]
