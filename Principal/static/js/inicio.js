document.getElementById("html").addEventListener("keydown", function (e) {

    if (e.code === 'Space') {
        generatePalette()
    }
});
function randomInteger(max) {
    return Math.floor(Math.random() * (max + 1));
}
function randomRgbColor() {
    let r = randomInteger(255);
    let g = randomInteger(255);
    let b = randomInteger(255);
    return [r, g, b];
}
function randomHexColor() {
    let [r, g, b] = randomRgbColor();

    let hr = r.toString(16).padStart(2, '0');
    let hg = g.toString(16).padStart(2, '0');
    let hb = b.toString(16).padStart(2, '0');
    return "#" + hr + hg + hb;
}
function generatePalette() {
    var highlightedItems = document.querySelectorAll('.color');

    console.log(highlightedItems.length)
    if (highlightedItems.length != 0) {
        highlightedItems.forEach(function (element) {
            element.remove();
        })
    }
    for (i = 0; i < 5; i++) {
        document.getElementById('paleta_colores').innerHTML += '<div class="color" style="background-color:' + randomHexColor() + ';width:300px;height:300px;margin:10px">' + randomHexColor() + '</div>'
    }
}
window.onload = function(){
    generatePalette()
}




function Mixcolor() {
    var highlightedItems = document.querySelectorAll('.colorofMix');
    if (highlightedItems.length != 0) {
        highlightedItems.forEach(function (element) {
            element.remove();
        })
    }
    color1 = document.getElementById('Mixcolor1').value
    color2 = document.getElementById('Mixcolor2').value
    var arrayColors = chroma.scale([color1, color2]).mode('lch').colors(6)
    for (var color of arrayColors) {
        document.getElementById('MixColors').innerHTML += "<div class='colorofMix' style='background-color:"+color+";width:300px;height:300px;margin:10px'>"+color+"/div>"
    }
}

