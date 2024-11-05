# pyPL

This project is a Python library for fetching and displaying stats from the Fantasy Premier League (FPL) API. It retrieves information about a specific FPL manager, including their team, points, ranking, favorite team id, and more.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Methods](#methods)
4. [Example](#example)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/rickykimani/pyPL.git
    ```

	```bash
	cd pyPL
    ```

	if you use vscode you can then type 
	```bash
	code .
	```

	to open in vscode.
	
	Then create your `main.py` file and also create a python environment `.venv`

2. **Install Required Packages**  
   This project requires `requests` for making HTTP requests to the API. Install it with:
   ```bash
   pip install requests
   ```


## Usage
To use this (not) library, import the Fpl class and create an instance with the manager ID of the FPL user you want to analyze. The class will fetch data from the API and provide methods for accessing various stats about the manager.

```bash
from fpl import Fpl

# Initialize FPL with a manager ID
manager_id = 1234567
team = Fpl(manager_id)

# Print summary information
print(team)
```
The `__str__` method is overridden to provide a quick summary of the manager's name and most recent event points.


## Methods
1.	**Constructor**

	`Fpl(managerID: int):` 
	
	Initializes the Fpl class with a manager's ID (a 7-digit integer) and fetches data from the FPL API.
2.	**Main Methods**
	General Info

	`id() -> int:` 
	  Returns the manager’s ID.
	
	`joined_time() -> datetime:` 
	Returns the date and time the manager joined FPL.

	`favorite_team() -> int:` 
	Returns the ID of the manager’s favorite team.

	`name() -> str:`
	Returns the team name.

	`player_first_name() -> str:` 
	Returns the manager’s first name.

	`player_last_name() ->str:` 
	Returns the manager’s last name.

	`player_region_name() -> str:` 
	Returns the manager's region name.

	### Performance and Ranking
	`summary_overall_points() -> int:` 
	Returns total points scored so far.

	`summary_overall_rank() -> int:` 
	Returns the overall ranking of the manager.

	`summary_event_points() -> int:` 
	Returns points scored in the most recent game week.

	`summary_event_rank() -> int:` 
	Returns the manager’s rank in the most recent game week.

	`current_event() -> int:` 
	Returns the current game week number.

	### Leagues
	`leagues() -> dict:` 
	Returns a JSON object containing all league information.

	`number_of_classic_leagues() -> int:` 
	Returns the number of classic leagues the manager has joined.

	`leagues_classic(n: int) -> dict:` 
	Returns data for the classic league at index n. Example Usage: team.leagues_classic(0)['name'] to get the league name.
	
3.	**Helper Methods (Internal Use Only)**

	`_checkStatusCode() -> bool:` 
	Verifies if the API response is successful (status code 200). Used internally for error handling.

### Error Handling
The library includes basic error handling for invalid inputs:

The constructor checks if managerID is a valid 7-digit integer.
Methods raise ValueError with informative messages for invalid inputs. For example, `leagues_classic(n)` raises an error if n is out of bounds.

## Example
Here’s a simple example to demonstrate usage:

```bash
from fpl import Fpl

# Initialize FPL with a manager ID
manager_id = 1234567
team = Fpl(manager_id)

# Access some information
print(f"Manager Name: {team.player_first_name()} {team.player_last_name()}")
print(f"Total Points: {team.summary_overall_points()}")
print(f"Joined Time: {team.joined_time()}")
print(f"Current Event Points: {team.summary_event_points()}")

# Get information on the first classic league
try:
    classic_league_info = team.leagues_classic(0)
    print(f"Classic League Name: {classic_league_info['name']}")
    print(f"Classic League ID: {classic_league_info['id']}")
except ValueError as e:
    print(e)
```
## Contributing
Contributions are welcome! If you’d like to add more methods or improve functionality, please fork the repository and create a pull request. Make sure to document any new methods in the README.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
