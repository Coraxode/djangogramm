window.like = function(url, post_id) {
    let stopper = false;
    $('#like-form_' + post_id).click( function(e) {
        if (stopper === true) {
            return;
        }
        stopper = true;

        e.preventDefault();
        let th = $(this);
        let image = th.find('img');
        let count_text = $('#count-form_' + post_id);
        let count = Number(count_text.text());

        $.ajax({
            url: url,
            type: 'POST',
            data: th.serialize(),
            success: function () {
                if (image.attr('src').includes('liked')){
                    image.attr('src', 'https://djangogramm-bucket-1.s3.eu-central-1.amazonaws.com/default_photos/like.png');
                    count_text.text(count - 1);
                } else {
                    image.attr('src', 'https://djangogramm-bucket-1.s3.eu-central-1.amazonaws.com/default_photos/liked.png');
                    count_text.text(count + 1);
                }
            }
        });
    });

};


