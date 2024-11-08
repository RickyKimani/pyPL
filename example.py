from fpl import FplCurrent, ClassicLeagues, ActivePhases, FplHistory

managerID =7612489

team = FplCurrent(managerID)
favorite_team_league = ClassicLeagues(team.managerID, 0)
favorite_team_league_active_phase_1 = ActivePhases(team.managerID, 0, 0)
history_gw_1 = FplHistory(team.managerID, 1)

#Printing the objects will be handled by the __str__ method
print("The following data is the data returned by the __str__ method of each class\n")
print(f"{team}\n")
print(f"{favorite_team_league}\n")
print(f"{favorite_team_league_active_phase_1}\n")
print(f"{history_gw_1}\n")