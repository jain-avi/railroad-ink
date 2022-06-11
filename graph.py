import numpy as np
from collections import deque

class CenterNode:
    def __init__(self, ):
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
        return "{}, {}, {}, {}".format(self.left_edge, self.top_edge, self.right_edge, self.bottom_edge)


class HorizontalEdgeNode:
    def __init__(self):
        self.type = "HorizontalEdgeNode"
        self.top_edge = None
        self.bottom_edge = None
        self.top_node = None
        self.bottom_node = None
        # For Graph Algorithms
        self.is_visited = False
        self.connected_component = None
        self.neighbors = []

    def set_top(self, top_edge, top_node):
        self.top_edge = top_edge
        self.top_node = top_node
        if top_node is not None:
            if top_edge == "Rail":
                self.neighbors.append((self.top_node, "Rail"))
            elif top_edge == "Road":
                self.neighbors.append((self.top_node, "Road"))
            else:
                pass

    def set_bottom(self, bottom_edge, bottom_node):
        self.bottom_edge = bottom_edge
        self.bottom_node = bottom_node
        if bottom_node is not None:
            if bottom_edge == "Rail":
                self.neighbors.append((self.bottom_node, "Rail"))
            elif bottom_edge == "Road":
                self.neighbors.append((self.bottom_node, "Road"))
            else:
                pass

    def is_connected(self):
        return (self.top_edge in ["Rail", "Road"]) or (self.bottom_edge in ["Rail", "Road"])

    def has_open_connection(self):
        if self.is_connected() == True:
            return (self.bottom_edge is None) or (self.top_edge is None)

    def __str__(self):
        return "{}, {}".format(self.top_edge, self.bottom_edge)


class VerticalEdgeNode:
    def __init__(self):
        self.type = "VerticalEdgeNode"
        self.left_edge = None
        self.right_edge = None
        self.left_node = None
        self.right_node = None
        # For Graph Algorithms
        self.is_visited = False
        self.connected_component = None
        self.neighbors = []

    def set_left(self, left_edge, left_node):
        self.left_edge = left_edge
        self.left_node = left_node
        if left_node is not None:
            if left_edge == "Rail":
                self.neighbors.append((self.left_node, "Rail"))
            elif left_edge == "Road":
                self.neighbors.append((self.left_node, "Road"))
            else:
                pass

    def set_right(self, right_edge, right_node):
        self.right_edge = right_edge
        self.right_node = right_node
        if right_node is not None:
            if right_edge == "Rail":
                self.neighbors.append((self.right_node, "Rail"))
            elif right_edge == "Road":
                self.neighbors.append((self.right_node, "Road"))
            else:
                pass

    def is_connected(self):
        return (self.left_edge in ["Rail", "Road"]) or (self.right_edge in ["Rail", "Road"])

    def has_open_connection(self):
        if self.is_connected() == True:
            return (self.left_edge is None) or (self.right_edge is None)

    def __str__(self):
        return "{}, {}".format(self.left_edge, self.right_edge)


class BoardGraph:
    def __init__(self):
        self.horizontal_edge_node_matrix = [[] for x in range(8)]
        for i in range(8):
            for j in range(7):
                temp_node = HorizontalEdgeNode()
                if i == 0:
                    temp_node.set_top("Edge", None)
                if i == 7:
                    temp_node.set_bottom("Edge", None)
                self.horizontal_edge_node_matrix[i].append(temp_node)
        self.horizontal_edge_node_matrix = np.array(self.horizontal_edge_node_matrix)

        self.vertical_edge_node_matrix = [[] for x in range(7)]
        for i in range(7):
            for j in range(8):
                temp_node = VerticalEdgeNode()
                if j == 0:
                    temp_node.set_left("Edge", None)
                if j == 7:
                    temp_node.set_right("Edge", None)

                self.vertical_edge_node_matrix[i].append(temp_node)
        self.vertical_edge_node_matrix = np.array(self.vertical_edge_node_matrix)

        self.center_node_matrix = [[] for x in range(7)]
        for i in range(7):
            for j in range(7):
                self.center_node_matrix[i].append(CenterNode())
        self.center_node_matrix = np.array(self.center_node_matrix)

        self.later_discovery_nodes = deque([]) #This is for discovery of nodes due to the overpass (That is a second network)


    def get_nodes(self, i, j): #Returns left, top, right, bottom, center for square i,j
        return self.vertical_edge_node_matrix[i][j],\
               self.horizontal_edge_node_matrix[i][j],\
               self.vertical_edge_node_matrix[i][j+1],\
               self.horizontal_edge_node_matrix[i+1][j],\
               self.center_node_matrix[i][j]


    def set_nodes_edges(self, i, j, top_face):
        left_node, top_node, right_node, bottom_node, center_node = self.get_nodes(i, j)
        if top_face.is_overpass == True:
            #I am assuming centre node connects to the road, and rail goes beneath (hence only diametrically opp nodes connect)
            if top_face.left_conn == "Road":
                left_node.set_right(top_face.left_conn, center_node)
                center_node.set_left(top_face.left_conn, left_node)

                right_node.set_left(top_face.right_conn, center_node)
                center_node.set_right(top_face.right_conn, right_node)

                top_node.set_bottom(top_face.top_conn, bottom_node)
                bottom_node.set_top(top_face.bottom_conn, top_node)

            else: #The top_conn is a Road then
                top_node.set_bottom(top_face.top_conn, center_node)
                center_node.set_top(top_face.top_conn, top_node)

                bottom_node.set_top(top_face.bottom_conn, center_node)
                center_node.set_bottom(top_face.bottom_conn, bottom_node)

                left_node.set_right(top_face.left_conn, right_node)
                right_node.set_left(top_face.right_conn, left_node)
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
        if node.type == "CenterNode":
            for neighbor in node.Road_neighbors + node.Rail_neighbors:
                neighbor_node, conn_type = neighbor
                if neighbor_node.is_visited == False:
                    self.run_DFS(neighbor_node, component_num)
        else:
            for neighbor in node.neighbors:
                neighbor_node, conn_type = neighbor
                if neighbor_node.is_visited == False:
                    self.run_DFS(neighbor_node, component_num)


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

        print(connected_component_dict)
        for node_lists in connected_component_dict.values():
            score += score_endpoints(len(node_lists))

        return score






