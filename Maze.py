import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

#BFS algrothms
class QueueFrontier():

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    ##remove beginning of the list
    def remove(self):
        if self.empty():
            raise Exception('empty frontier')
        else:
            node =self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():

    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.walls = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def solve(self):
        """Finds a solution to maze if one exists"""

        #keep track of number of state explored
        self.num_explored =0

        #Initialize frontier to just the starting positon
        start =Node(state =self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        #Initialize on empty explored set
        self.explored = set()

        #keep looping until solution found
        while True:

            #if nothing left in frontier then no path
            if frontier.empty():
                raise Exception('no solution')

            #choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            #if node is the goal then we have a solution
            if node.state == self.goal:
                actions =[]
                cells =[]
                #follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return

            #Mark node as explored
            self.explored.add(node.state)

            #Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state =state, parent=node,action=action)
                    frontier.add(child)

if __name__ == "__main__":
    # Initialize maze
    m = Maze(r"C:\Users\xafro\OneDrive - Alexandria University\intro AI\AI project\mazefile.TXT")
    #BFS solution
    m.solve()
    print("Solution path: ")
    m.print()

