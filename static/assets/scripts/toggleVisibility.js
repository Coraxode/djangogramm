window.toggleVisibility = function(id) {
    const div1 = document.getElementById("div_tags_" + id);
    const div2 = document.getElementById("div_change_tags_" + id);

    if (div1 && div2) {
        if (div1.style.display === "none") {
            div1.style.display = "flex";
            div2.style.display = "none";
        } else {
            div1.style.display = "none";
            div2.style.display = "flex";
        }
    }
}
