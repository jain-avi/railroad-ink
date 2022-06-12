from graph import CenterNode, HorizontalEdgeNode, VerticalEdgeNode, BoardGraph

G = BoardGraph()

conn = "Rail"

h1 = HorizontalEdgeNode(0,3)
h2 = HorizontalEdgeNode(0,1)
h3 = HorizontalEdgeNode(-2,-1)
h4 = HorizontalEdgeNode(-4,-1)
h5 = HorizontalEdgeNode(-2,-3)
h6 = HorizontalEdgeNode(-2,-5)

x1 = CenterNode(0,2)
x2 = CenterNode(0,0)
x3 = CenterNode(-2,0)
x4 = CenterNode(-4,0)
x5 = CenterNode(-4,-2)
x6 = CenterNode(-2,-2)
x7 = CenterNode(-2,-4)

v1 = VerticalEdgeNode(1,0)
v2 = VerticalEdgeNode(-1,0)
v3 = VerticalEdgeNode(-3,0)
v4 = VerticalEdgeNode(-3,-2)
v5 = VerticalEdgeNode(-1,-4)


h1.set_bottom(conn, x1)

x1.set_top(conn, h1)
x1.set_bottom(conn, h2)

h2.set_top(conn, x1)
h2.set_bottom(conn, x2)

x2.set_top(conn, h2)
x2.set_right(conn, v1)
x2.set_left(conn, v2)

v1.set_left(conn, x2)

v2.set_right(conn, x2)
v2.set_left(conn, x3)

x3.set_right(conn, v2)
x3.set_left(conn, v3)
x3.set_bottom(conn, h3)

h3.set_top(conn, x3)
h3.set_bottom(conn, x6)

v3.set_right(conn, x3)
v3.set_left(conn, x4)

x4.set_right(conn, v3)
x4.set_bottom(conn, h4)

h4.set_top(conn, x4)
h4.set_bottom(conn, x5)

x5.set_top(conn, h4)
x5.set_right(conn, v4)

v4.set_left(conn, x5)
v4.set_right(conn, x6)

x6.set_top(conn, h3)
x6.set_left(conn, v4)
x6.set_bottom(conn, h5)

h5.set_top(conn, x6)
h5.set_bottom(conn, x7)

x7.set_top(conn, h5)
x7.set_right(conn, v5)
x7.set_bottom(conn, h6)

v5.set_left(conn, x7)

h6.set_top(conn, x7)

#lp = G.longest_path_of_unvisited(h1, [], "Rail")

#for node in lp:
 #   print(node)

node_list = [h1, h2, h3, h4, h5, h6, x1, x2, x3, x4, x5, x6, x7, v1, v2, v3, v4, v5]

lp = G.find_longest_path(node_list, "Rail")
print(G.process_list_of_nodes(lp))

