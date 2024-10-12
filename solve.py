class BoardState:
    def __init__(self, board):
        self.board = [row[:] for row in board]

    def display(self):
        for row in self.board:
            print(" ".join(map(str, row)))
        print()

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))


class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth


class PuzzleSolver:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def iterative_deepening(self):
        depth_limit = 0
        while True:
            visited = set()
            result = self.depth_limited_search(Node(self.start_state, None, 0), depth_limit, visited)
            if result is not None:
                return result
            depth_limit += 1

    def depth_limited_search(self, current_node, limit, visited):
        if current_node.state == self.goal_state:
            return current_node
        elif current_node.depth == limit:
            return None
        else:
            successors = self.generate_successors(current_node)
            for successor in successors:
                if successor.state not in visited:
                    visited.add(successor.state)
                    result = self.depth_limited_search(successor, limit, visited)
                    if result is not None:
                        return result
            return None

    def generate_successors(self, current_node):
        successors = []
        empty_row, empty_col = next((r, c) for r in range(3) for c in range(3) if current_node.state.board[r][c] == 0)

        moves = [
            (empty_row - 1, empty_col),  # Up
            (empty_row + 1, empty_col),  # Down
            (empty_row, empty_col - 1),  # Left
            (empty_row, empty_col + 1)   # Right
        ]

        for new_row, new_col in moves:
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = [row[:] for row in current_node.state.board]
                new_board[empty_row][empty_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[empty_row][empty_col]
                
                new_state = BoardState(new_board)
                new_node = Node(new_state, current_node, current_node.depth + 1)
                successors.append(new_node)

        return successors

    def print_solution_path(self, node):
        path = []
        while node is not None:
            path.append(node)
            node = node.parent
        for n in reversed(path):
            n.state.display()


class PuzzleSolverModified(PuzzleSolver):
    def generate_successors(self, current_node):
        successors = []
        empty_row, empty_col = next((r, c) for r in range(3) for c in range(3) if current_node.state.board[r][c] == 0)

        moves = [
            (empty_row - 1, empty_col),  # Up
            (empty_row + 1, empty_col),  # Down
            (empty_row, empty_col - 1),  # Left
            (empty_row, empty_col + 1)   # Right
        ]

        for new_row, new_col in moves:
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = [row[:] for row in current_node.state.board]
                new_board[empty_row][empty_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[empty_row][empty_col]
                
                new_state = BoardState(new_board)
                new_node = Node(new_state, current_node, current_node.depth + 1)
                successors.append(new_node)

        return successors


if __name__ == "__main__":
    # Estado inicial
    initial_board = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    start_state = BoardState(initial_board)

    # Estado objetivo
    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    goal_state = BoardState(goal_board)

    solver_copy = PuzzleSolver(start_state, goal_state)
    import time
    start_time_copy = time.time()
    solution_copy = solver_copy.iterative_deepening()
    end_time_copy = time.time()

    if solution_copy:
        print("Solução encontrada (Cópia e Edição):")
        solver_copy.print_solution_path(solution_copy)
        print(f"Tempo de execução: {(end_time_copy - start_time_copy) * 1000:.2f} ms\n")
    else:
        print("Nenhuma solução encontrada (Cópia e Edição).\n")

    solver_modified = PuzzleSolverModified(start_state, goal_state)
    start_time_modified = time.time()
    solution_modified = solver_modified.iterative_deepening()
    end_time_modified = time.time()

    if solution_modified:
        print("Solução encontrada (Modificação Direta):")
        solver_modified.print_solution_path(solution_modified)
        print(f"Tempo de execução: {(end_time_modified - start_time_modified) * 1000:.2f} ms")
    else:
        print("Nenhuma solução encontrada (Modificação Direta).")
