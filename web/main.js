init();
function init() {
    var height = 9
    var width = 9;
    var table = document.getElementsByTagName("table")[0]
    console.log(table)

    for (var x = 0; x < height; x++) {
        var tr = document.createElement("tr")
        table.appendChild(tr)
        for (var y = 0; y < width; y++) {
            var td = document.createElement("td")
            table.appendChild(td)
            for(var z=2;z<5;z=z+2){
                if( ((x==z-1 || x == height-z ) && y>=z-1 && y<=height-z) || ((y==z-1 || y == height-z ) && x>=z-1 && x<=height-z)){
                    var treasure = document.getElementsByTagName("td")[x*width+y]
                    treasure.classList.add("walls")
                }
            }
        }
    }
    var treasure = document.getElementsByTagName("td")[Math.floor((height*width)/2)]
    treasure.classList.add("treasure")
}