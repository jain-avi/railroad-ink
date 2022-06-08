
class CenterNode:
    def __init__(self):
        self.left_edge, self.top_edge, self.right_edge, self.bottom_edge = None, None, None, None
        self.left = None
        self.top = None
        self.right = None
        self.bottom = None

    def set_edges(self, left, top, right, bottom):
        self.left_edge, self.top_edge, self.right_edge, self.bottom_edge = left, top, right, bottom

    def set_left_node(self, left):
        self.left = left

    def set_top_node(self, top):
        self.top = top

    def set_right_node(self, right):
        self.right = right

    def set_bottom_node(self, bottom):
        self.bottom = bottom


class HorizontalEdgeNode:
    def __init__(self):
        self.top_edge = None
        self.bottom_edge = None

    def set_top_edge(self, top):
        self.top_edge = top

    def set_bottom_edge(self, bottom):
        self.bottom_edge = bottom

    def set_top_node(self, top):
        self.top = top

    def set_bottom_node(self, bottom):
        self.bottom = bottom


class VerticalEdgeNode:
    def __init__(self):
        self.left = None
        self.right = None

    def set_left_edge(self, left):
        self.left_edge = left

    def set_right_edge(self, right):
        self.right_edge = right

    def set_left_node(self, left):
        self.left = left

    def set_right_node(self, right):
        self.right = right


class BoardGraph:
    def __init__(self):
        self.horizontal_edge_node_matrix = [[] for x in range(8)]
        for i in range(8):
            for j in range(7):
                temp_node = HorizontalEdgeNode()
                if i == 0:
                    temp_node.set_top_edge("Edge")
                if i == 7:
                    temp_node.set_bottom_edge("Edge")
                self.horizontal_edge_node_matrix[i].append(temp_node)

        self.vertical_edge_node_matrix = [[] for x in range(7)]
        for i in range(7):
            for j in range(8):
                temp_node = VerticalEdgeNode()
                if j == 0:
                    temp_node.set_left_edge("Edge")
                if j == 7:
                    temp_node.set_right_edge("Edge")

                self.vertical_edge_node_matrix[i].append(temp_node)

        self.center_node_matrix = [[] for x in range(7)]
        for i in range(7):
            for j in range(7):
                self.center_node_matrix[i].append(CenterNode())


    def get_nodes(self, i, j): #Returns left, top, right, bottom, center for square i,j
        return self.vertical_edge_node_matrix[i][j],\
               self.horizontal_edge_node_matrix[i][j],\
               self.vertical_edge_node_matrix[i][j+1],\
               self.horizontal_edge_node_matrix[i+1][j],\
               self.center_node_matrix[i][j]


    def set_nodes_edges(self, i, j, top_face):
        left_node, top_node, right_node, bottom_node, center_node = get_nodes(i, j)

        if top_face.left_conn != "Empty":
            left_node.set_right_edge(top_face.left_conn)
            left_node.set_right_node(center_node)
            center_node.set_left_node(left_node)

        if top_face.top_conn != "Empty":
            top_node.set_bottom_edge(top_face.top_conn)
            top_node.set_bottom_node(center_node)
            center_node.set_top_node(top_node)

        if top_face.right_conn != "Empty":
            right_node.set_left_edge(top_face.right_conn)
            right_node.set_left_node(center_node)
            center_node.set_right_node(right_node)

        if top_face.bottom_conn != "Empty":
            bottom_node.set_top_edge(top_face.bottom_conn)
            bottom_node.set_top_node(center_node)
            center_node.set_bottom_node(bottom_node)






