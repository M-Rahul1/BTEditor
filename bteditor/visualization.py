import json
import matplotlib.pyplot as plt
import numpy as np
import time

class Node:
    def __init__(self, node_data):
        self.id = node_data["id"]
        self.title = node_data["title"]
        self.pos_x = node_data["pos_x"]
        self.pos_y = node_data["pos_y"]

    def __str__(self):
        return f"{self.title} (ID: {self.id})"


class Edge:
    def __init__(self, edge_data):
        self.start = edge_data["start"]
        self.end = edge_data["end"]

    def __str__(self):
        return f"Edge: {self.start} -> {self.end}"


def load_data_from_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    nodes = [Node(node_data) for node_data in data["nodes"]]
    edges = [Edge(edge_data) for edge_data in data["edges"]]
    return nodes, edges


def visualize(nodes, edges):
    fig, ax = plt.subplots()

    # Plot nodes
    for i, node in enumerate(nodes):
        node_plot = ax.plot(node.pos_x, node.pos_y, marker="o", markersize=10, color="blue")[0]
        ax.text(node.pos_x, node.pos_y, node.title, fontsize=12, ha="center", va="bottom")
        plt.draw()
        plt.pause(2)  # Delay for 2 seconds
        node_plot.set_color("yellow")  # Change color to yellow while running
        plt.draw()
        plt.pause(2)  # Delay for 2 seconds
        node_plot.set_color("green")  # Change color to green after node is processed
        plt.draw()

    # Plot edges
    for i, edge in enumerate(edges):
        start_node = next((node for node in nodes if node.id == edge.start), None)
        end_node = next((node for node in nodes if node.id == edge.end), None)
        if start_node and end_node:
            edge_plot = ax.plot([start_node.pos_x, end_node.pos_x], [start_node.pos_y, end_node.pos_y], color="blue")[0]
            plt.draw()
            plt.pause(2)  # Delay for 2 seconds
            edge_plot.set_color("yellow")  # Change color to yellow while running
            plt.draw()
            plt.pause(2)  # Delay for 2 seconds
            edge_plot.set_color("green")  # Change color to green after edge is processed
            plt.draw()

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Graph Visualization")
    ax.grid(True)
    plt.show()


if __name__ == "__main__":
    json_file = "example.json"
    nodes, edges = load_data_from_json(json_file)
    visualize(nodes, edges)