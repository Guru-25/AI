import heapq
import matplotlib.pyplot as plt
import networkx as nx

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x  # x-coordinate on map (for visualization)
        self.y = y  # y-coordinate on map (for visualization)

class AStar:
    def __init__(self, cities, roads):
        self.cities = cities
        self.roads = roads
        
        # Create a graph representation
        self.graph = {}
        for city in cities:
            self.graph[city.name] = {}
        
        for source, dest, distance, time in roads:
            self.graph[source][dest] = (distance, time)
            self.graph[dest][source] = (distance, time)  # Assuming bidirectional roads
    
    def heuristic(self, city1_name, city2_name, h_type='distance'):
        """
        Calculate heuristic between cities
        h_type: 'distance' or 'time'
        """
        city1 = next(city for city in self.cities if city.name == city1_name)
        city2 = next(city for city in self.cities if city.name == city2_name)
        
        # Simple Euclidean distance as heuristic
        return ((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2) ** 0.5
    
    def find_path(self, start, goal, h_type='distance'):
        """
        Find path from start city to goal city using A* algorithm
        h_type: 'distance' or 'time' (heuristic and cost type to optimize)
        """
        # Index for cost tuple based on heuristic type
        h_index = 0 if h_type == 'distance' else 1
        
        open_set = []
        heapq.heappush(open_set, (0, start))  # (f_score, city_name)
        
        came_from = {}
        
        g_score = {city: float('inf') for city in self.graph}
        g_score[start] = 0
        
        f_score = {city: float('inf') for city in self.graph}
        f_score[start] = self.heuristic(start, goal, h_type)
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, g_score[goal]
            
            for neighbor in self.graph[current]:
                # g_score is the cost from start to neighbor through current
                temp_g_score = g_score[current] + self.graph[current][neighbor][h_index]
                
                if temp_g_score < g_score[neighbor]:
                    # Found a better path
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, goal, h_type)
                    
                    # Add to open set if not already there
                    if not any(neighbor == item[1] for item in open_set):
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None, None  # No path found

def visualize_path(cities, roads, path, title):
    """Visualize the cities, roads and optimal path"""
    G = nx.Graph()
    
    # Create a mapping from city name to city object
    city_dict = {city.name: city for city in cities}
    
    # Add nodes (cities)
    for city in cities:
        G.add_node(city.name, pos=(city.x, city.y))
    
    # Add edges (roads)
    for source, dest, distance, time in roads:
        G.add_edge(source, dest, distance=distance, time=time)
    
    # Get positions for all nodes
    pos = nx.get_node_attributes(G, 'pos')
    
    plt.figure(figsize=(12, 10))
    
    # Draw all nodes and edges
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)
    
    # Highlight the path
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
        
        # Add edge labels for the path
        edge_labels = {}
        for source, dest in path_edges:
            distance = G[source][dest]['distance']
            time = G[source][dest]['time']
            edge_labels[(source, dest)] = f"{distance}km, {time}hr"
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    # Add Tamil Nadu outline or background (simplified)
    plt.title(title)
    plt.axis('off')
    
    # Add a legend
    plt.plot([], [], 'b-', label='Roads')
    plt.plot([], [], 'r-', linewidth=3, label='Optimal Path')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_')}.png", dpi=300)
    plt.show()

def main():
    # Define cities with coordinates (approximate for visualization)
    cities = [
        City("Chennai", 100, 80),
        City("Coimbatore", 20, 40),
        City("Madurai", 50, 20),
        City("Trichy", 60, 40),
        City("Salem", 50, 60),
        City("Tirunelveli", 40, 10),
        City("Vellore", 80, 90)
    ]
    
    # Define roads: (source, destination, distance in km, time in hours)
    roads = [
        ("Chennai", "Vellore", 140, 2.5),
        ("Chennai", "Trichy", 330, 6),
        ("Vellore", "Salem", 180, 3.5),
        ("Salem", "Coimbatore", 160, 3),
        ("Salem", "Trichy", 145, 2.8),
        ("Trichy", "Madurai", 140, 2.7),
        ("Madurai", "Tirunelveli", 160, 3),
        ("Coimbatore", "Madurai", 210, 4),
        ("Trichy", "Coimbatore", 220, 4.2)
    ]
    
    astar = AStar(cities, roads)
    
    # Find path optimizing for distance
    start_city = "Chennai"
    goal_city = "Tirunelveli"
    
    path_distance, total_distance = astar.find_path(start_city, goal_city, 'distance')
    print(f"\nOptimal path by distance from {start_city} to {goal_city}:")
    print(" -> ".join(path_distance))
    print(f"Total distance: {total_distance} km")
    
    # Visualize path optimized for distance
    visualize_path(cities, roads, path_distance, f"A* Path (Distance): {start_city} to {goal_city}")
    
    # Find path optimizing for time
    path_time, total_time = astar.find_path(start_city, goal_city, 'time')
    print(f"\nOptimal path by time from {start_city} to {goal_city}:")
    print(" -> ".join(path_time))
    print(f"Total time: {total_time} hours")
    
    # Visualize path optimized for time
    visualize_path(cities, roads, path_time, f"A* Path (Time): {start_city} to {goal_city}")

if __name__ == "__main__":
    main()