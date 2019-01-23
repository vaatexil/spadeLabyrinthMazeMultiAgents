init();
function init() {
    var height = 9;
    var width = 9;
    var table = document.getElementsByTagName("table")[0]
    for (var x = 0; x < height; x++) {
        var tr = document.createElement("tr")
        table.appendChild(tr)
        for (var y = 0; y < width; y++) {
            var td = document.createElement("td")
            table.appendChild(td)
        }
    }
}

function updateClassMaze(maze){
    var height = maze.length
    var classes = ["none","walls","doors","treasure","scout","slave", "engi"]
    for (var x = 0; x < height; x++) {
        for (var y = 0; y < height; y++) {
            var td = document.getElementsByTagName("td")[x*height+y]
            td.classList=classes[maze[x][y][0]]
            td.cellIndex
        }
    }

}