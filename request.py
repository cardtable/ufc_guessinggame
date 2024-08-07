#!/usr/bin/env python3
# process_csv.py
#doesnt need to be run unless there's an update with the csv file
import csv
import json
from graph_module import Graph

def read_csv_reverse(file_path):
    with open(file_path, 'r') as file:
        reader = list(csv.DictReader(file))
        return reader[::-1]

def process_csv_to_json(csv_file_path, output_file_path):
    rows = read_csv_reverse(csv_file_path)
    graph = Graph()

    for row in rows:
        red_fighter = row['r_fighter']
        blue_fighter = row['b_fighter']
        winner = row['winner']

        # Determine the winner's name
        if winner == 'Red':
            winner_name = red_fighter
        elif winner == 'Blue':
            winner_name = blue_fighter
        else:
            winner_name = 'Draw'  # Handle cases where there is no clear winner

        graph.add_node(red_fighter)
        graph.add_node(blue_fighter)
        graph.add_opps(red_fighter, blue_fighter, winner_name)

    fighters_data = {}

    for fighter_name, node in graph.nodes.items():
        fighters_data[fighter_name] = {
            'name': fighter_name,
            'opponents': [opponent.name for opponent in node.opponents],
            'rematches': node.rematches
        }

    with open(output_file_path, 'w') as json_file:
        json.dump(fighters_data, json_file, indent=4)
    print(f"Data has been written to {output_file_path}")

# Example usage
if __name__ == "__main__":
    csv_file_path = 'large_dataset.csv'  # Replace with your actual CSV file path
    output_file_path = 'fighters_data.json'  # Replace with your desired output file path
    process_csv_to_json(csv_file_path, output_file_path)
