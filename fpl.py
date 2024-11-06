# Written by Ricky Kimani
## Nov.2024

import requests
from datetime import datetime
from dataclasses import dataclass

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
        except requests.JSONDecodeError:
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
    
    @dataclass
    class ClassicLeagues:
        def __init__(self, classic_league : dict) -> None:
            if not isinstance(classic_league, dict):
                raise TypeError("Invalid constructor type, you must pass in a dict containing the classic league you want the data for!")
            self.classic_league = classic_league

        def __str__(self) -> str:
            return f"League: {self.name()}\nID: {self.id()}"

        def id(self) -> int:
            return self.classic_league["id"]
        
        def name(self) -> str:
            return self.classic_league["name"]
        
        def short_name(self) -> str:
            return self.classic_league["short_name"]
        
        def created(self) -> datetime:
            return datetime.strptime(self.classic_league["created"], "%Y-%m-%dT%H:%M:%S.%fZ")
        
        def closed(self) -> bool:
            return self.classic_league["closed"]
        
        def rank(self):
            return self.classic_league["rank"]
        
        def max_entries(self):
            return self.classic_league["max_entries"]
        
        def league_type(self) -> str:
            return self.classic_league["league_type"]
        
        def scoring(self) -> str:
            return self.classic_league["scoring"]
        
        def admin_entry(self):
            return self.classic_league["admin_entry"]
        
        def start_event(self) -> int:
            return self.classic_league["start_event"]
        
        def entry_can_leave(self) -> bool:
            return self.classic_league["entry_can_leave"]
        
        def entry_can_admin(self) -> bool:
            return self.classic_league["entry_can_admin"]
        
        def entry_can_invite(self) -> bool:
            return self.classic_league["entry_can_invite"]
        
        def has_cup(self) -> bool:
            return self.classic_league["has_cup"]
        
        def cup_league(self):
            return self.classic_league["cup_league"]
        
        def cup_qualified(self):
            return self.classic_league["cup_qualified"]
        
        def rank_count(self) -> int:
            return self.classic_league["rank_count"]
        
        def entry_percentile_rank(self) -> int:
            return self.classic_league["entry_percentile_rank"]
        
        def number_of_active_phases(self) -> int:
            return len(self.classic_league["active_phases"])
        
        def active_phases(self, n:int) -> dict:
            if not isinstance(n, int) or n < 0 or n >= self.number_of_active_phases():
                raise ValueError(f"Error, {n} is not valid. Use a number between 0 and {self.number_of_active_phases() - 1}")
            return self.classic_league["active_phases"][n]
        
        @dataclass
        class ActivePhase:
            def __init__(self, _phase:dict) -> None:
                if not isinstance(_phase, dict):
                    raise TypeError("Invalid constructor type, you must pass in a dict containing the active phase you want the data for!")
                self._phase = _phase
            
            def __str__(self) -> str:
                return f"phase: {self.phase()}\nrank: {self.rank()}\nlast rank: {self.last_rank()}"
            
            def phase(self) -> int:
                return self._phase["phase"]
            
            def rank(self) -> int:
                return self._phase["rank"]
            
            def last_rank(self) -> int:
                return self._phase["last_rank"]
            
            def rank_sort(self) -> int:
                return self._phase["rank_sort"]
            
            def total(self) -> int:
                return self._phase["total"]
            
            def league_id(self) -> int:
                return self._phase["league_id"]
            
            def rank_count(self):
                return self._phase["rank_count"]
            
            def entry_percentile_rank(self):
                return self._phase["entry_percentile_rank"]
            


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