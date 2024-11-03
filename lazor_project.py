class Block:
    """A basic class"""

    def interact(self, laser):
        pass


class ReflectiveBlock(Block):
    """Reflection block, reverse the laser direction"""

    def interact(self, laser):
        laser.vx = -laser.vx
        laser.vy = -laser.vy


class OpaqueBlock(Block):
    """Transparent block to block lasers"""

    def interact(self, laser):
        laser.active = False


class RefractiveBlock(Block):
    """The refracting block changes the direction of the laser and continues to propagate"""

    def interact(self, laser):
        laser.vx, laser.vy = -laser.vy, laser.vx  # 例如，简单折射规则  


class Laser:
    """Laser class, defining position, direction and activity state"""

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.active = True


class LazorGame:
    """Game class, parses.bff file and initializes game state"""

    def __init__(self, bff_path):
        self.board = []
        self.lasers = []
        self.targets = set()
        self.parse_bff(bff_path)

    def parse_bff(self, file_path):
        """Parses.bff files to read grid, block, laser and target point information"""
        with open(file_path, 'r') as file:
            grid_active = False
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                elif line == "GRID START":
                    grid_active = True
                    continue
                elif line == "GRID STOP":
                    grid_active = False
                    continue

                if grid_active:
                    row = []
                    for char in line:
                        if char == 'A':
                            row.append(ReflectiveBlock())
                        elif char == 'B':
                            row.append(OpaqueBlock())
                        elif char == 'C':
                            row.append(RefractiveBlock())
                        else:
                            row.append(None)
                    self.board.append(row)
                elif line[0] in "L":
                    _, x, y, vx, vy = line.split()
                    self.lasers.append(Laser(int(x), int(y), int(vx), int(vy)))
                elif line[0] in "P":
                    _, x, y = line.split()
                    self.targets.add((int(x), int(y)))

    def get_block_at(self, x, y):
        """Gets the block at the specified location"""
        if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]):
            return self.board[x][y]
        return None


class LazorSolver:
    """Solver class that searches to find the laser path of all target points"""

    def __init__(self, game):
        self.game = game
        self.solution_path = []

    def is_target_hit(self, laser):
        """Determine whether the laser has hit the target point"""
        return (laser.x, laser.y) in self.game.targets

    def solve(self):
        """Use recursion or backtracking algorithms to find solutions"""
        for laser in self.game.lasers:
            if self.trace_laser_path(laser):
                return True
        return False

    def trace_laser_path(self, laser):
        """Trace the laser path, recording each step and checking to see if all target points were hit"""
        path = []
        visited_positions = set()
        while laser.active:
            laser.x += laser.vx
            laser.y += laser.vy

            # Check if the line has been crossed
            if not (0 <= laser.x < len(self.game.board) and 0 <= laser.y < len(self.game.board[0])):
                laser.active = False
                break

            current_position = (laser.x, laser.y)
            path.append(current_position)

            # Check to see if the target point is hit
            if self.is_target_hit(laser):
                self.solution_path.append(path)
                return True

            # If the location has already been visited, stop at the optimized speed
            if current_position in visited_positions:
                break
            visited_positions.add(current_position)

            # Interaction with blocks
            block = self.game.get_block_at(laser.x, laser.y)
            if block:
                block.interact(laser)

        return False


def output_solution(solution_path, output_file="solution mad_1.txt"):
    """Output the solution to the specified file"""
    with open(output_file, 'w') as file:
        for path in solution_path:
            file.write("Path:\n")
            for (x, y) in path:
                file.write(f"({x}, {y})\n")
            file.write("\n")
        file.write("Solution complete. All targets hit.\n")


if __name__ == "__main__":
    game = LazorGame(r"D:\lazor_fall_2024\bff_files\mad_1.bff")
    solver = LazorSolver(game)

    if solver.solve():
        output_solution(solver.solution_path)
        print("Solution found! Check solution.txt for details.")
    else:
        print("No solution found.")