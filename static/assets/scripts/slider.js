window.right = function(slider_id) {
    let a = $('#photos_scroll_' + slider_id);
    let number = (a.children().length - 1) * 475;

    if (Number(a.css('right').replace('px', '')) < number && a.queue().length === 0) {
        a.animate({right: '+=475px', left: '-=475px'}, 320);
    }
}

window.left = function(slider_id) {
    let a = $('#photos_scroll_' + slider_id);

    if (Number(a.css('right').replace('px', '')) >= 475 && a.queue().length === 0) {
        a.animate({right: '-=475px', left: '+=475px'}, 320);
    }
}