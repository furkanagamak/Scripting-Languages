def contain_virus(grid)
    rows_of_grid = grid.size
    columns_of_grid = grid[0].size
    
    total_num_of_walls = 0

    # helper function to check if the cell is out of bounds or empty
    def is_out_of_bounds_or_empty(first_index, second_index, rows_of_grid, columns_of_grid, grid)
        return true if first_index < 0 || first_index >= rows_of_grid || second_index < 0 || second_index >= columns_of_grid
        grid[first_index][second_index] == 0
    end

    # go through each cell in the grid
    grid.each_with_index do |row_of_grid, first_index|
        row_of_grid.each_with_index do |cell_of_row, second_index|
            # check if the cell has a virus
            if cell_of_row == 1
                # check surrounding cells
                [[-1, 0], [1, 0], [0, -1], [0, 1]].each do |row_change, column_change|
                    total_num_of_walls += 1 if is_out_of_bounds_or_empty(first_index + row_change, second_index + column_change, rows_of_grid, columns_of_grid, grid)
                end
            end
        end
    end
    total_num_of_walls
end

isInfected = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]

# Call the function and store the result in a variable
result = contain_virus(isInfected)

# Print the result
puts "Number of walls needed: #{result}"