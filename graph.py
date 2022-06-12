import numpy as np
import copy

class CenterNode:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.type = "CenterNode"
        self.left_edge, self.top_edge, self.right_edge, self.bottom_edge = None, None, None, None
        self.left_node, self.top_node, self.right_node, self.bottom_node = None, None, None, None
        #For Graph Algorithms
        self.is_visited = False
        self.connected_component = None
        self.Road_neighbors = []
        self.Rail_neighbors = []

    def set_left(self, left_edge, left_node):
        self.left_edge = left_edge
        self.left_node = left_node
        if left_node is not None:
            if left_edge == "Rail":
                self.Rail_neighbors.append((self.left_node, "Rail"))
            elif left_edge == "Road":
                self.Road_neighbors.append((self.left_node, "Road"))
            else:
                pass

    def set_top(self, top_edge, top_node):
        self.top_edge = top_edge
        self.top_node = top_node
        if top_node is not None:
            if top_edge == "Rail":
                self.Rail_neighbors.append((self.top_node, "Rail"))
            elif top_edge == "Road":
                self.Road_neighbors.append((self.top_node, "Road"))
            else:
                pass

    def set_right(self, right_edge, right_node):
        self.right_edge = right_edge
        self.right_node = right_node
        if right_node is not None:
            if right_edge == "Rail":
                self.Rail_neighbors.append((self.right_node, "Rail"))
            elif right_edge == "Road":
                self.Road_neighbors.append((self.right_node, "Road"))
            else:
                pass

    def set_bottom(self, bottom_edge, bottom_node):
        self.bottom_edge = bottom_edge
        self.bottom_node = bottom_node
        if bottom_node is not None:
            if bottom_edge == "Rail":
                self.Rail_neighbors.append((self.bottom_node, "Rail"))
            elif bottom_edge == "Road":
                self.Road_neighbors.append((self.bottom_node, "Road"))
            else:
                pass

    def is_connected(self):
        return (self.left_edge is not None) or (self.top_edge is not None) or (self.right_edge is not None) or (self.bottom_edge is not None)

    def __str__(self):
        return "[{},{}] | {}, {}, {}, {}".format(self.i, self.j, self.left_edge, self.top_edge, self.right_edge, self.bottom_edge)


class HorizontalEdgeNode:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.type = "HorizontalEdgeNode"
        self.top_edge = None
        self.bottom_edge = None
        self.top_node = None
        self.bottom_node = None
        # For Graph Algorithms
        self.is_visited = False
        self.connected_component = None
        self.neighbors = []
        self.type_connection = None

    def set_top(self, top_edge, top_node):
        self.top_edge = top_edge
        self.top_node = top_node
        if top_node is not None:
            if top_edge == "Rail":
                self.neighbors.append((self.top_node, "Rail"))
                self.type_connection = "Rail"
            elif top_edge == "Road":
                self.neighbors.append((self.top_node, "Road"))
                self.type_connection = "Road"
            else:
                pass

    def set_bottom(self, bottom_edge, bottom_node):
        self.bottom_edge = bottom_edge
        self.bottom_node = bottom_node
        if bottom_node is not None:
            if bottom_edge == "Rail":
                self.neighbors.append((self.bottom_node, "Rail"))
                self.type_connection = "Rail"
            elif bottom_edge == "Road":
                self.neighbors.append((self.bottom_node, "Road"))
                self.type_connection = "Road"
            else:
                pass

    def is_connected(self):
        return (self.top_edge in ["Rail", "Road"]) or (self.bottom_edge in ["Rail", "Road"])

    def has_open_connection(self):
        if self.is_connected() == True:
            return (self.bottom_edge is None) or (self.top_edge is None)

    def __str__(self):
        return "[{},{}] | {}, {}".format(self.i, self.j, self.top_edge, self.bottom_edge)


class VerticalEdgeNode:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.type = "VerticalEdgeNode"
        self.left_edge = None
        self.right_edge = None
        self.left_node = None
        self.right_node = None
        # For Graph Algorithms
        self.is_visited = False
        self.connected_component = None
        self.neighbors = []
        self.type_connection = None #Can either be Rail or Road

    def set_left(self, left_edge, left_node):
        self.left_edge = left_edge
        self.left_node = left_node
        if left_node is not None:
            if left_edge == "Rail":
                self.neighbors.append((self.left_node, "Rail"))
                self.type_connection = "Rail"
            elif left_edge == "Road":
                self.neighbors.append((self.left_node, "Road"))
                self.type_connection = "Road"
            else:
                pass

    def set_right(self, right_edge, right_node):
        self.right_edge = right_edge
        self.right_node = right_node
        if right_node is not None:
            if right_edge == "Rail":
                self.neighbors.append((self.right_node, "Rail"))
                self.type_connection = "Rail"
            elif right_edge == "Road":
                self.neighbors.append((self.right_node, "Road"))
                self.type_connection = "Road"
            else:
                pass

    def is_connected(self):
        return (self.left_edge in ["Rail", "Road"]) or (self.right_edge in ["Rail", "Road"])

    def has_open_connection(self):
        if self.is_connected() == True:
            return (self.left_edge is None) or (self.right_edge is None)

    def __str__(self):
        return "[{},{}] | {}, {}".format(self.i, self.j, self.left_edge, self.right_edge)


class BoardGraph:
    def __init__(self):
        self.horizontal_edge_node_matrix = [[] for x in range(8)]
        for i in range(8):
            for j in range(7):
                temp_node = HorizontalEdgeNode(i, j)
                if i == 0:
                    temp_node.set_top("Edge", None)
                if i == 7:
                    temp_node.set_bottom("Edge", None)
                self.horizontal_edge_node_matrix[i].append(temp_node)
        self.horizontal_edge_node_matrix = np.array(self.horizontal_edge_node_matrix)

        self.vertical_edge_node_matrix = [[] for x in range(7)]
        for i in range(7):
            for j in range(8):
                temp_node = VerticalEdgeNode(i, j)
                if j == 0:
                    temp_node.set_left("Edge", None)
                if j == 7:
                    temp_node.set_right("Edge", None)

                self.vertical_edge_node_matrix[i].append(temp_node)
        self.vertical_edge_node_matrix = np.array(self.vertical_edge_node_matrix)

        self.center_node_matrix = [[] for x in range(7)]
        for i in range(7):
            for j in range(7):
                self.center_node_matrix[i].append(CenterNode(i, j))
        self.center_node_matrix = np.array(self.center_node_matrix)

        self.connected_components = {} #Dict that will store component id, along with nodes

        self.level2_center_nodes = []


    def process_list_of_nodes(self, node_list):
        temp_list = []
        for node in node_list:
            temp_list.append((node.i, node.j))

        return temp_list


    def get_nodes(self, i, j): #Returns left, top, right, bottom, center for square i,j
        return self.vertical_edge_node_matrix[i][j],\
               self.horizontal_edge_node_matrix[i][j],\
               self.vertical_edge_node_matrix[i][j+1],\
               self.horizontal_edge_node_matrix[i+1][j],\
               self.center_node_matrix[i][j]


    def set_nodes_edges(self, i, j, top_face):
        left_node, top_node, right_node, bottom_node, center_node = self.get_nodes(i, j)
        if top_face.is_overpass == True:
            hidden_center_node = CenterNode(i, j)
            self.level2_center_nodes.append(hidden_center_node)
            #I am assuming centre node connects to the road, and rail goes beneath (hence only diametrically opp nodes connect)
            if top_face.left_conn == "Road":
                left_node.set_right(top_face.left_conn, center_node)
                center_node.set_left(top_face.left_conn, left_node)

                right_node.set_left(top_face.right_conn, center_node)
                center_node.set_right(top_face.right_conn, right_node)

                top_node.set_bottom(top_face.top_conn, hidden_center_node)
                hidden_center_node.set_top(top_face.top_conn, top_node)

                bottom_node.set_top(top_face.bottom_conn, hidden_center_node)
                hidden_center_node.set_bottom(top_face.bottom_conn, bottom_node)

            else: #The top_conn is a Road then
                top_node.set_bottom(top_face.top_conn, center_node)
                center_node.set_top(top_face.top_conn, top_node)

                bottom_node.set_top(top_face.bottom_conn, center_node)
                center_node.set_bottom(top_face.bottom_conn, bottom_node)

                left_node.set_right(top_face.left_conn, hidden_center_node)
                hidden_center_node.set_left(top_face.left_conn, left_node)

                right_node.set_left(top_face.right_conn, hidden_center_node)
                hidden_center_node.set_right(top_face.right_conn, right_node)
        else:
            if top_face.left_conn != "Empty":
                left_node.set_right(top_face.left_conn, center_node)
                center_node.set_left(top_face.left_conn, left_node)

            if top_face.top_conn != "Empty":
                top_node.set_bottom(top_face.top_conn, center_node)
                center_node.set_top(top_face.top_conn, top_node)

            if top_face.right_conn != "Empty":
                right_node.set_left(top_face.right_conn, center_node)
                center_node.set_right(top_face.right_conn, right_node)

            if top_face.bottom_conn != "Empty":
                bottom_node.set_top(top_face.bottom_conn, center_node)
                center_node.set_bottom(top_face.bottom_conn, bottom_node)

    def score_middle_squares(self): #Find how many middle squares are used
        #print("Scoring Middle Squares")
        score = 0
        for i in range(2,5):
            for j in range(2,5):
                if self.center_node_matrix[i][j].is_connected() == True:
                    score += 1
        return score


    def score_open_connections(self): #Open ended components
        score = 0
        #print("Horizontal")
        for i in range(8):
            for j in range(7):
                if self.horizontal_edge_node_matrix[i][j].has_open_connection() == True:
                    score -= 1
        #print("Vertical")
        for i in range(7):
            for j in range(8):
                if self.vertical_edge_node_matrix[i][j].has_open_connection() == True:
                    score -= 1

        return score


    def run_DFS(self, node, component_num):
        node.is_visited = True
        node.connected_component = component_num
        if component_num not in self.connected_components:
            self.connected_components[component_num] = [node]
        else:
            self.connected_components[component_num].append(node)

        if node.type == "CenterNode":
            neighbor_list = node.Road_neighbors + node.Rail_neighbors
        else:
            neighbor_list = node.neighbors

        for neighbor in neighbor_list:
            neighbor_node, conn_type = neighbor
            if neighbor_node.is_visited == False:
                self.run_DFS(neighbor_node, component_num)


    def longest_path_of_unvisited(self, node, visited_list, conn_type):
        if node is None:
            return visited_list
        else:
            new_visited_list = visited_list + [node]
            neighbor_list = getattr(node, "{}_neighbors".format(conn_type)) if node.type=="CenterNode" else node.neighbors
            neighbors_to_explore = [x for x,y in neighbor_list if x not in visited_list]
            temp_max_list = new_visited_list
            for neighbor in neighbors_to_explore:
                new_list = self.longest_path_of_unvisited(neighbor, new_visited_list, conn_type)
                if len(new_list) > len(temp_max_list):
                    temp_max_list = new_list
            return temp_max_list


    def find_longest_path(self, node_list, conn_type):
        hor_ver_nodes = [node for node in node_list if (node.type != "CenterNode" and node.type_connection == conn_type)]

        longest_path = []
        for node in hor_ver_nodes:
            print(node)
            if node.type == "HorizontalEdgeNode":
                path1 = self.longest_path_of_unvisited(node.top_node, [], conn_type)
                path2 = self.longest_path_of_unvisited(node.bottom_node, [], conn_type)
            else:
                path1 = self.longest_path_of_unvisited(node.left_node, [], conn_type)
                path2 = self.longest_path_of_unvisited(node.right_node, [], conn_type)

            #print("Path1", self.process_list_of_nodes(path1))
            #print("Path2", self.process_list_of_nodes(path2))
            unique_path1 = set(path1)
            unique_path2 = set(path2)

            intersection = unique_path1.intersection(unique_path2)

            #print("Intersection", self.process_list_of_nodes(intersection))

            if len(intersection) > 0:
                #print("Contains Common Nodes, Path Nullified")
                temp_longest_path = []
            else:
                temp_longest_path = path1[::-1] + [node] + path2

            if len(temp_longest_path) > len(longest_path):
                longest_path = temp_longest_path

        return longest_path


    def find_longest_road_rail(self):
        longest_road = []
        longest_rail = []
        for component_num in self.connected_components:
            temp_longest_road = self.find_longest_path(self.connected_components[component_num], "Road")
            if len(temp_longest_road) > len(longest_road):
                longest_road = temp_longest_road

            temp_longest_rail = self.find_longest_path(self.connected_components[component_num], "Rail")
            if len(temp_longest_rail) > len(longest_rail):
                longest_rail = temp_longest_rail

        longest_road = [node for node in longest_road if node.type == "CenterNode"]
        print("Longest Road")
        print(self.process_list_of_nodes(longest_road))
        longest_rail = [node for node in longest_rail if node.type == "CenterNode"]
        print("Longest Rail")
        print(self.process_list_of_nodes(longest_rail))
        return len(longest_road), len(longest_rail)


    def label_connected_components(self):
        component_num = 1
        for node in self.center_node_matrix.flatten():
            if node.is_visited == False:
                if node.is_connected() == True:
                    self.run_DFS(node, component_num)
                    component_num += 1


    def score_connected_ends(self):
        score = 0
        horizontal_edge_nodes = [(0,1), (0,3), (0,5),
                                 (7,1), (7,3), (7,5)]
        vertical_edge_nodes = [(1,0),(3,0),(5,0),
                               (1,7),(3,7),(5,7)]

        #These are edge nodes, so they only have one connected component
        connected_component_dict = {}
        def add_to_dict(node, i,j):
            if node.connected_component not in connected_component_dict:
                connected_component_dict[node.connected_component] = [(i,j)]
            else:
                connected_component_dict[node.connected_component].append((i,j))

        def score_endpoints(num_endpoints):
            if num_endpoints <= 11:
                return (num_endpoints - 1)*4
            else:
                return 45

        for i,j in horizontal_edge_nodes:
            if self.horizontal_edge_node_matrix[i][j].connected_component is not None:
                add_to_dict(self.horizontal_edge_node_matrix[i][j], i, j)

        for i, j in vertical_edge_nodes:
            if self.vertical_edge_node_matrix[i][j].connected_component is not None:
                add_to_dict(self.vertical_edge_node_matrix[i][j], i ,j)

        for node_lists in connected_component_dict.values():
            score += score_endpoints(len(node_lists))

        return score






