class DFS:
    def __init__(self):
        self.nodes_expanded = 0
    
    def solve(self,grid):
        return self._dfs(grid,0)
    
    def _dfs(self, grid, index):
        grid.__str__()
        self.nodes_expanded += 1

        if index == grid.rows*grid.cols:
            if grid.is_goal():
                return grid
            return None
        r = index // grid.cols
        c = index % grid.cols

        original_rotation = grid.grid[r][c].rotation

        for rot in range(4):
            grid.grid[r][c].rotation = rot
            # Pruning
            if grid.partial_valid(r,c):
                result = self._dfs(grid,index+1)
                if result:
                    return result
        grid.grid[r][c].rotation = original_rotation
        return None



