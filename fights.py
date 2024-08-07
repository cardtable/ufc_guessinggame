#!/usr/bin/env python3
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx


class Node:
    def __init__(self, name, image_path=None):
        self.name = name
        self.opponents = []
        self.rematches = {}  # stores all fight results
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

    def display_graph(self):
        for node in self.nodes.values():
            connections = [neighbor.name for neighbor in node.opponents]
            print(f"{node.name} is connected to: {', '.join(connections)}")
            rematches = node.rematches
            for opponent_name, results in rematches.items():
                print(f"Rematches against {opponent_name}: {', '.join(results)}")
    
    def display_graph_with_images(self):
        G = nx.Graph()
        for node in self.nodes.values():
            G.add_node(node.name)
            for opponent in node.opponents:
                G.add_edge(node.name, opponent.name)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=False, node_size=500, node_color='w', edge_color='gray')
        for node_name, node in self.nodes.items():
            if node.image_path:
                (x, y) = pos[node_name]
                img = mpimg.imread(node.image_path)
                plt.imshow(img, extent=(x-0.1, x+0.1, y-0.1, y+0.1), zorder=1)
        for node_name, (x, y) in pos.items():
            plt.text(x, y, node_name, fontsize=12, ha='center', zorder=2, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
        plt.show()
        
    def get_fight_result(self, fighter1_name, fighter2_name, fight_number):
        if fighter1_name in self.nodes and fighter2_name in self.nodes:
            results = self.nodes[fighter1_name].rematches.get(fighter2_name, [])
            if 0 < fight_number <= len(results):
                return results[fight_number - 1]
            else:
                return f"No record for fight {fight_number} between {fighter1_name} and {fighter2_name}."
        return "fighters not found."

    def read_json_and_generate_graph(json_file_path):
        script_dir = Path(__file__).parent
        image_dir = script_dir / 'images'
        
        with open(json_file_path, 'r') as json_file:
            fighters_data = json.load(json_file)
        
        graph = Graph()

        # First, ensure all fighters are added as nodes
        for fighter_name in fighters_data:
            image_filename = fighter_name.replace(" ", "_")
            image_path = None
            for ext in ['jpeg', 'webp', 'png']:
                temp_path = image_dir / f"{image_filename}.{ext}"
                if temp_path.exists():
                    image_path = str(temp_path)
                    break
            graph.add_node(fighter_name, image_path=image_path)

        # Second, add only existing nodes as opponents
        for fighter_name, data in fighters_data.items():
            for opponent_name in data['opponents']:
                if opponent_name in fighters_data:  # Only add if opponent is also a listed fighter
                    for result in data['rematches'][opponent_name]:
                        graph.add_opps(fighter_name, opponent_name, result)

        return graph

if __name__ == "__main__":
    json_file_path = 'fighters_data.json'
    graph = Graph.read_json_and_generate_graph(json_file_path)
    

    result = graph.get_fight_result("Brandon Moreno", "Alexandre Pantoja", 1)
    print(f"Result of the 1st fight: {result}")
    

    
    result = graph.get_fight_result("Chael Sonnen", "Jon Jones", 1)
    print(f"Result of the 1st fight: {result}")
    
    
    


 