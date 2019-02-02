function updateClassMaze(maze){
    var height = maze.length
    var classes = ["none","walls","doors","treasure","scout","engi", "slave"]
    for (var x = 0; x < height; x++) {
        for (var y = 0; y < height; y++) {
            var td = document.getElementsByTagName("td")[x*height+y]
            td.classList=classes[maze[x][y][0]]
            td.cellIndex
        }
    }

}