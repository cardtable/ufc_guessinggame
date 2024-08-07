#!/usr/bin/env python3
class Node:
    def __init__(self, name, image_path=None):
        self.name = name
        self.opponents = []
        self.rematches = {}  # Stores all fight results, not only rematches
        self.image_path = image_path

    def __repr__(self):
        return f"Node({self.name})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name, image_path=None):
        if name not in self.nodes:
            self.nodes[name] = Node(name, image_path)

    def add_opps(self, node1_name, node2_name, winner):
        if node1_name in self.nodes and node2_name in self.nodes:
            self.nodes[node1_name].opponents.append(self.nodes[node2_name])
            self.nodes[node2_name].opponents.append(self.nodes[node1_name])

            if node2_name not in self.nodes[node1_name].rematches:
                self.nodes[node1_name].rematches[node2_name] = []
            if node1_name not in self.nodes[node2_name].rematches:
                self.nodes[node2_name].rematches[node1_name] = []

            self.nodes[node1_name].rematches[node2_name].append(winner)
            self.nodes[node2_name].rematches[node1_name].append(winner)  # storing all results

    def get_fight_result(self, fighter1_name, fighter2_name, fight_number):
        if fighter1_name in self.nodes and fighter2_name in self.nodes:
            results = self.nodes[fighter1_name].rematches.get(fighter2_name, [])
            if 0 < fight_number <= len(results):
                return results[fight_number - 1]
            else:
                return f"No record for fight {fight_number} between {fighter1_name} and {fighter2_name}."
        return "fighters not found."

    def display_graph(self):
        for node in self.nodes.values():
            connections = [neighbor.name for neighbor in node.opponents]
            print(f"{node.name} is connected to: {', '.join(connections)}")
            rematches = node.rematches
            for opponent_name, results in rematches.items():
                print(f"Rematches against {opponent_name}: {', '.join(results)}")
