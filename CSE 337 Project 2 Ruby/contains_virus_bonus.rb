require 'set'

class Region
    attr_accessor :infected, :uninfected, :walls

    def initialize
        @infected = Set.new
        @uninfected = Set.new
        @walls = 0
    end
end

def contain_virus_bonus(is_infected)
    total_num_of_walls = 0

    while true
        visited_indices_of_grid = Set.new
        regions_of_grid = []

        is_infected.each_with_index do |row_of_grid, first_index|
            row_of_grid.each_with_index do |cell_of_row, second_index|
                if cell_of_row == 1 && !visited_indices_of_grid.include?([first_index, second_index])
                    region_of_grid = Region.new
                    depth_first_search_of_grid(first_index, second_index, is_infected, visited_indices_of_grid, region_of_grid)
                    regions_of_grid << region_of_grid
                end
            end
        end

        break if regions_of_grid.empty?

        max_number_of_uninfected_grids = -1
        max_value_of_indices_of_region = -1

        regions_of_grid.each_with_index do |region_of_grid, first_index|
            if region_of_grid.uninfected.size > max_number_of_uninfected_grids
                max_number_of_uninfected_grids = region_of_grid.uninfected.size
                max_value_of_indices_of_region = first_index
            end
        end

        if max_number_of_uninfected_grids == 0
            break
        end

        total_num_of_walls += regions_of_grid[max_value_of_indices_of_region].walls

        regions_of_grid[max_value_of_indices_of_region].infected.each do |first_index, second_index|
            is_infected[first_index][second_index] = -1
        end

        regions_of_grid.each_with_index do |region_of_grid, first_index|
            next if first_index == max_value_of_indices_of_region
            region_of_grid.infected.each do |first_index, second_index|
                [[1, 0], [-1, 0], [0, 1], [0, -1]].each do |new_row_change, new_column_change|
                    new_first_index = first_index + new_row_change
                    new_second_index = second_index + new_column_change
                    if new_first_index >= 0 && new_first_index < is_infected.length && new_second_index >= 0 && new_second_index < is_infected[0].length && is_infected[new_first_index][new_second_index] == 0
                        is_infected[new_first_index][new_second_index] = 1
                    end
                end
            end
        end
    end
    total_num_of_walls
end

def depth_first_search_of_grid(first_index, second_index, dfs_grid, visited_indices_of_grid, dfs_region)
    return if first_index < 0 || first_index >= dfs_grid.length || second_index < 0 || second_index >= dfs_grid[0].length || visited_indices_of_grid.include?([first_index, second_index])
    visited_indices_of_grid.add([first_index, second_index])

    if dfs_grid[first_index][second_index] == 1
        dfs_region.infected.add([first_index, second_index])
        [[1, 0], [-1, 0], [0, 1], [0, -1]].each do |row_change, column_change|
            new_first_index = first_index + row_change
            new_second_index = second_index + column_change
            if new_first_index >= 0 && new_first_index < dfs_grid.length && new_second_index >= 0 && new_second_index < dfs_grid[0].length
                if dfs_grid[new_first_index][new_second_index] == 0
                    dfs_region.uninfected.add([new_first_index, new_second_index])
                    dfs_region.walls += 1
                elsif dfs_grid[new_first_index][new_second_index] == 1
                    depth_first_search_of_grid(new_first_index, new_second_index, dfs_grid, visited_indices_of_grid, dfs_region)
                end
            end
        end
    end
end

# Example input, where 1 represents infected cells and 0 represents uninfected cells:
# isInfected = [
#   [0, 1, 0, 0, 1],
#   [0, 1, 0, 0, 1],
#   [0, 0, 0, 0, 1]
# ]

isInfected = [[0,1,0,0,0,0,0,1],[0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]]

# Call the function and store the result in a variable
result = contain_virus_bonus(isInfected)

# Print the result
puts "Number of walls needed: #{result}"