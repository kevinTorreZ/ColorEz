function randomHexColor() {
    let [r, g, b] = randomRgbColor();

    let hr = r.toString(16).padStart(2, '0');
    let hg = g.toString(16).padStart(2, '0');
    let hb = b.toString(16).padStart(2, '0');

    for (i = 0; i < 5; i++) {
        document.getElementById('paleta_colores').innerHTML += '<div style="background-color:#' + toString(hr) + toString(hg) + toString(hb) + ';width:300px,height:300px></div>'
    }
}
document.getElementById("html").addEventListener("keydown", function (e) {
    console.log(e.key)
    if (e.keyCode === 32) {
        console.log("a")
        document.getElementById("btnhiden").click();
    }
});
document.getElementById("btnhiden").onclick = function () {
    console.log("a")
    randomHexColor()
}