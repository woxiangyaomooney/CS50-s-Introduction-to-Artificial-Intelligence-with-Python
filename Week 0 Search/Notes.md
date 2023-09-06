## Search   
- BFS   
- DFS  
python实现方式：   
Repeat:    
1. If the frontier is empty,    
   - Stop. There is no solution to the problem.
2. Remove a node from the frontier.This is the node that will be considered.    
3. If the node contains the goal state,    
   - Return the solution. Stop.    
Else,     
      * Expand the node (find all the new nodes that could be reached from this node), and add resulting nodes to the frontier.
      * Add the current node to the explored set.
```
{
import sys

class Node(): #结点
    def __init__(self, state, parent, action): #python中类的属性是通过“__init__”来创建的，每个成员函数的参数都要有self参数，表示函数自身
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier(): #dfs堆栈
    def __init__(self): #创建空列表
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier) 
        #any(...): 这是一个Python内置函数 any()，它接受一个可迭代对象（如列表或生成器）并检查其中是否存在至少一个为 True 的元素。如果存在至少一个为 True 的元素，any() 函数将返回 True，否则返回 False。
        #整个代码行的目的是检查 self.frontier 中是否至少有一个节点的状态等于给定的 state，如果有，则返回 True，否则返回 False。这在搜索算法等场景中很有用，以确定某个状态是否已经被探索过。
    def empty(self):
        return len(self.frontier) == 0 #若空则返回True

    def remove(self):
        if self.empty():
            raise Exception("empty frontier") 
            #异常抛出语句。异常用于指示在程序执行期间发生了某种错误或不正常情况。当程序执行到 raise 语句时，它会立即停止执行当前代码块，并开始寻找与抛出的异常匹配的异常处理程序。如果没有找到匹配的异常处理程序，程序将终止并显示异常消息，告知您发生了什么错误。
        else:
            node = self.frontier[-1] #移出最后一个node,堆栈先进后出
            self.frontier = self.frontier[:-1] #更新frontier
            return node


class QueueFrontier(StackFrontier): #继承StackFrontier类的成员和属性

    def remove(self): #重覆盖remove()
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] #移出第一个node
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = [] #Bool列表，记录全部墙的位置
        for i in range(self.height):
            row = [] #Bool列表，记录每一行墙的位置
            for j in range(self.width): # “A“”B“” “表示此处没有墙，记为False,否则表示有墙，记为True
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
        # solution 被赋值为 None，表示它当前没有指向任何对象或值。
        # None 在 Python 中是一个特殊的值，表示空或缺失。通常情况下，None 用于初始化变量，或者在需要定义一个占位符但暂时没有具体值的情况下使用。


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
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
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier() #dfs，修改成QueueFrontier则是bfs
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set() #初始化空集合，而self.explored = {}则表示创建一个空字典

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal: #成功之后再回溯
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw #画图
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
}
```

## Greedy Best-First Search
### A* Search   
![image](https://github.com/woxiangyaomooney/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/assets/134345191/94d56378-2044-451e-b7ae-f027e88d11a3)   
optimal if
- h(n) is admissible (never overestimates the
true cost), and
- h(n) is consistent (for every node n and
successor n' with step cost c, h(n) ≤ h(n') + c)

## Adversarial Search
### Minimax 
两个选手，一个为了使值更高，一个为了使值更低   
计算所有情况，从下到上赋值 
![image](https://github.com/woxiangyaomooney/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/assets/134345191/182d4188-c682-4abb-b023-852589f5dc3c)

Representing a Tic-Tac-Toe AI:

S₀: Initial state (in our case, an empty 3X3 board)
- Players(s): a function that, given a state s, returns which player’s turn it is (X or O).
- Actions(s): a function that, given a state s, return all the legal moves in this state (what spots are free on the board).
- Result(s, a): a function that, given a state s and action a, returns a new state. This is the board that resulted from performing the action a on state s (making a move in the game).
- Terminal(s): a function that, given a state s, checks whether this is the last step in the game, i.e. if someone won or there is a tie. Returns True if the game has ended, False otherwise.
- Utility(s): a function that, given a terminal state s, returns the utility value of the state: -1, 0, or 1.

![image](https://github.com/woxiangyaomooney/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/assets/134345191/428e0cad-c10e-418d-813a-f5619d39578e)   
![image](https://github.com/woxiangyaomooney/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/assets/134345191/9b03b5ad-8264-4fe7-b919-a7f868c02859)
![image](https://github.com/woxiangyaomooney/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/assets/134345191/5d050118-145f-4ab6-bfec-f85189a55cb1)

### Alpha-Beta Pruning
![image](https://github.com/woxiangyaomooney/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/assets/134345191/0be886c8-4ec5-48ac-82aa-79c12ed882b9)

### Depth-Limited Minimax
