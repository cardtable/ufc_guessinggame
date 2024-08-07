#!/usr/bin/env python3
import fights
import json
popular_fighters = ["Islam Makhachev", "Conor McGregor", "Jon Jones", "Tony Ferguson", "Khabib Nurmagomedov", "Rafael Dos Anjos", "Georges St-Pierre",
                    "Nate Diaz", "Nick Diaz", "Alex Pereira", "Demetrious Johnson", "Henry Cejudo", "Sean O'Malley", "Aljomain Sterling", "Jose Aldo", 
                    "BJ Penn", "Brandon Moreno", "Alexandre Pantoja", "Dominick Cruz", "TJ Dillashaw", "Petr Yan", "Cody Garbrandt", "Merab Dvalishvili",
                    "Marlon Vera", "Deiveson Figueiredo", ""]
def check_typo_for_popular_fighters():
    try:
        with open('fighters_data.json', 'r') as file:
            fighters_data = json.load(file)
    except FileNotFoundError:
        print("The file fighters_data.json was not found.")
        fighters_data = {}
    except json.JSONDecodeError:
        print("Error decoding JSON from the file fighters_data.json.")
        fighters_data = {}
    not_found_fighters = [fighter for fighter in popular_fighters if fighter not in fighters_data]
    if not_found_fighters:
        print("Fighters not found in the JSON file:")
        for fighter in not_found_fighters:
            print(fighter)
    else:
        print("All popular fighters are present in the JSON file.")

check_typo_for_popular_fighters()