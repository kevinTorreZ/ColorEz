

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
    dicc = ['('+r+','+g+','+b+')',"#" + hr + hg + hb]
    return dicc;
}
function generatePalette() {
    var highlightedItems = document.querySelectorAll('.color');
    if (highlightedItems.length != 0) {
        highlightedItems.forEach(function (element) {
            element.remove();
        })
    }
    for (i = 0; i < 6; i++) {
        var obj = randomHexColor();
        document.getElementById('paleta_colores').innerHTML += '<div class="color" style="background-color:'  + obj[1].toString() + ';width:250px;height:500px;margin:10px">' + "<div class='textos'>" + "<div class='text1'>" + '<h1>HEX: ' + obj[1].toString() + '</h1>' + '</div>' + "<div class='text2'>" + '<h1>RGB: ' + obj[0].toString() + '</h1>' + "</div>" + "</div>" +  '</div>'
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
    var arrayColors = chroma.scale([color1, color2]).mode('lch').colors(10)
    for (var color of arrayColors) {
        document.getElementById('MixColors').innerHTML += "<div class='colorofMix' style='background-color:"+color+";width:170px;height:300px;color:white;'>" +  "<div class='texto-color'>" + "<h1>" + color + "</h1>" + "</div>" + "</div>"
    }
}

window.onload = function(){
    var rnd1 = randomHexColor()
    var rnd2 = randomHexColor()
    document.getElementById('Mixcolor1').value = rnd1[1].toString()
    document.getElementById('Mixcolor2').value = rnd2[1].toString()
    Mixcolor()
}
