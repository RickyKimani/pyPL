# Written by Ricky Kimani
## Nov.2024

# MIT License

# Copyright (c) 2024 rickykimani

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests
from datetime import datetime
from dataclasses import dataclass


class FplCurrent:
    def __init__(self, managerID: int) -> None:
        self.managerID = managerID
        if not isinstance(managerID, int) or len(str(managerID)) != 7:
            raise ValueError(
                "Invalid manager ID. A manager ID must be a 7-digit integer."
            )

        self._url = f"https://fantasy.premierleague.com/api/entry/{managerID}/"
        self._response = requests.get(self._url)

        # Check for response status code
        if not self._checkStatusCode():
            raise ConnectionError(
                f"Failed to retrieve data. Status code: {self._response.status_code}"
            )

        try:
            self._jsonResponse = self._response.json()
        except requests.JSONDecodeError:
            raise ValueError("Invalid response format: Response is not JSON.")
        self.id = self._jsonResponse["id"]
        self.joined_time = datetime.strptime(
            self._jsonResponse["joined_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.started_event = self._jsonResponse["started_event"]
        self.player_first_name = self._jsonResponse["player_first_name"]
        self.player_last_name = self._jsonResponse["player_last_name"]
        self.player_region_id = self._jsonResponse["player_region_id"]
        self.player_region_name = self._jsonResponse["player_region_name"]
        self.player_region_iso_code_short = self._jsonResponse[
            "player_region_iso_code_short"
        ]
        self.player_region_iso_code_long = self._jsonResponse[
            "player_region_iso_code_long"
        ]
        self.years_active = self._jsonResponse["years_active"]
        self.summary_overall_points = self._jsonResponse["summary_overall_points"]
        self.summary_overall_rank = self._jsonResponse["summary_overall_rank"]
        self.summary_event_points = self._jsonResponse["summary_event_points"]
        self.summary_event_rank = self._jsonResponse["summary_event_rank"]
        self.current_event = self._jsonResponse["current_event"]
        self.leagues = self._jsonResponse["leagues"]
        self.number_of_classic_leagues = len(self.leagues.get("classic", []))

        self.name = self._jsonResponse["name"]
        self.name_change_blocked = self._jsonResponse["name_change_blocked"]
        self.entered_events = self._jsonResponse["entered_events"]
        self.kit = self._jsonResponse["kit"]
        self.last_deadline_bank = self._jsonResponse["last_deadline_bank"]
        self.last_deadline_value = self._jsonResponse["last_deadline_value"]
        self.last_deadline_total_transfers = self._jsonResponse[
            "last_deadline_total_transfers"
        ]
        self.favorite_team = self.leagues_classic(0)["name"]

    def __str__(self) -> str:
        return f"{self.name}, {self.summary_event_points} points\nFavorite team: {self.favorite_team}"

    def _checkStatusCode(self) -> bool:
        status_code = self._response.status_code
        if status_code != 200:
            print("Error:", status_code)
            return False
        return True

    def leagues_classic(self, n: int):
        if not isinstance(n, int) or n < 0 or n >= self.number_of_classic_leagues:
            raise ValueError(
                f"Error, {n} is not valid. Use a number between 0 and {self.number_of_classic_leagues - 1}"
            )
        return self.leagues["classic"][n]

@dataclass
class ClassicLeagues(FplCurrent):
    def __init__(self, managerID, n: int):
        super().__init__(managerID)
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        elif n < 0 or n >= self.number_of_classic_leagues:
            raise ValueError(
                f"n must be a number between 0 ~ {self.number_of_classic_leagues - 1}"
            )
        self.n = n
        self.league = self.leagues_classic(n)

        self.C_id = self.league["id"]
        self.C_name = self.league["name"]
        self.short_name = self.league["short_name"]
        self.created = datetime.strptime(
            self.league["created"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.closed = self.league["closed"]
        self.rank = self.league["rank"]
        self.max_entries = self.league["max_entries"]
        self.league_type = self.league["league_type"]
        self.scoring = self.league["scoring"]
        self.admin_entry = self.league["admin_entry"]
        self.start_event = self.league["start_event"]
        self.entry_can_leave = self.league["entry_can_leave"]
        self.entry_can_admin = self.league["entry_can_admin"]
        self.entry_can_invite = self.league["entry_can_invite"]
        self.has_cup = self.league["has_cup"]
        self.cup_league = self.league["cup_league"]
        self.cup_qualified = self.league["cup_qualified"]
        self.rank_count = self.league["rank_count"]
        self.entry_percentile_rank = self.league["entry_percentile_rank"]
        self.number_of_active_phases = len(self.league["active_phases"])

    def __str__(self):
        return f"Name: {self.C_name}\nId: {self.C_id}"

    def active_phases(self, n: int) -> dict:
        if not isinstance(n, int) or n < 0 or n >= self.number_of_active_phases:
            raise ValueError(
                f"Error, {n} is not valid. Use a number between 0 and {self.number_of_active_phases - 1}"
            )
        return self.league["active_phases"][n]

@dataclass
class ActivePhases(ClassicLeagues):
    def __init__(self, managerID, n, phase_number):
        super().__init__(managerID, n)
        if not isinstance(phase_number, int):
            raise TypeError(
                "Phase number is an integer, pass in ClassicLeagues.number_of_active_phases()"
            )
        elif n < 0 or n >= self.number_of_active_phases:
            raise ValueError(f"Enter n between 0 ~ {self.number_of_active_phases - 1}")
        self.phase_number = phase_number
        self.active_phase = self.active_phases(self.phase_number)

        self.phase = self.active_phase["phase"]
        self.A_rank = self.active_phase["rank"]
        self.last_rank = self.active_phase["last_rank"]
        self.rank_sort = self.active_phase["rank_sort"]
        self.total = self.active_phase["total"]
        self.league_id = self.active_phase["league_id"]
        self.A_rank_count = self.active_phase["rank_count"]
        self.A_entry_percentile_rank = self.active_phase["entry_percentile_rank"]

    def __str__(self) -> str:
        return f"phase: {self.phase}\nrank: {self.rank}\nlast rank: {self.last_rank}"

@dataclass
class FplHistory:
    def __init__(self, managerID: int, gameWeek: int):
        # Validate the managerID
        self.managerID = managerID
        if not isinstance(managerID, int) or len(str(managerID)) != 7:
            raise ValueError(
                "Invalid manager ID. A manager ID must be a 7-digit integer."
            )

        # Validate gameweek
        self.gameWeek = gameWeek
        if not isinstance(self.gameWeek, int) or self.gameWeek < 1:
            raise ValueError("Gameweek must be an integer greater than or equal to 1.")

        self._url = f"https://fantasy.premierleague.com/api/entry/{managerID}/history/"
        self._response = requests.get(self._url)

        # Check for response status code
        if not self._checkStatusCode():
            raise ConnectionError(
                f"Failed to retrieve data. Status code: {self._response.status_code}"
            )

        # Try to get JSON response
        try:
            self._jsonResponse = self._response.json()
            self.gameWeeks_played = len(self._jsonResponse["current"])
        except requests.JSONDecodeError:
            raise ValueError("Invalid response format: Response is not JSON.")

        # Validate if gameweek exists in the JSON data
        if not self.checkValidgameWeek():
            raise ValueError(f"Gameweek {self.gameWeek} is not available in the data.")

        # Store the JSON data for the specified gameweek
        self.gameweek_data = self.get_gameweek_data()
        #self.gameweek_data = np.array(self.gameweek_data, dtype=object)

        self.event = self.gameweek_data["event"]
        self.points = self.gameweek_data["points"]
        self.total_points = self.gameweek_data["total_points"]
        self.rank = self.gameweek_data["rank"]
        self.rank_sort = self.gameweek_data["rank_sort"]
        self.overall_rank = self.gameweek_data["overall_rank"]
        self.percentile_rank = self.gameweek_data["percentile_rank"]
        self.bank = self.gameweek_data["bank"]
        self.value = self.gameweek_data["value"]
        self.event_transfers = self.gameweek_data["event_transfers"]
        self.event_transfers_cost = self.gameweek_data["event_transfers_cost"]
        self.points_on_bench = self.gameweek_data["points_on_bench"]

    def __str__(self):
        # This is an optional method to represent the object as a string
        return f"FplHistory(managerID={self.managerID}, gameWeek={self.gameWeek})"

    def _checkStatusCode(self) -> bool:
        # Checks the response status code
        if self._response.status_code != 200:
            print(f"Error: Received status code {self._response.status_code}")
            return False
        return True

    def checkValidgameWeek(self):
        # Validate if the requested gameweek exists in the data
        gameWeeks_played = len(self._jsonResponse["current"])
        if self.gameWeek < 1 or self.gameWeek > gameWeeks_played:
            return False
        return True

    def get_gameweek_data(self):
        # Retrieves the JSON data for the specified gameweek
        # The "current" key contains the data for all the gameweeks played.
        # Each element in the list corresponds to one gameweek.
        gameWeeks_played = len(self._jsonResponse["current"])
        if self.gameWeek <= gameWeeks_played:
            return self._jsonResponse["current"][
                self.gameWeek - 1
            ]  # Gameweek is 1-indexed
        else:
            raise ValueError(
                f"Gameweek {self.gameWeek} is out of range. Valid gameweeks are 1-{gameWeeks_played}."
            )

    def __str__(self):
        return f"Gameweek: {self.event}\nPoints: {self.points}\nTotal points: {self.total_points}\nPoints on bench : {self.points_on_bench}\nPercentile rank: {self.percentile_rank}"