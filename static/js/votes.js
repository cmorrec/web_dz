$('.js-vote').click(function(ev) {
    if ($(this).hasClass('disabled') == true)
        return;

    var ctx = new Map(); ;
    if ($(this).parent().hasClass('box-qst') == true)
        ctx['like'] = 'question';
    else if ($(this).parent().hasClass('box-answer') == true)
        ctx['like'] = 'answer';
    console.log("like " + ctx['like']);
    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        id = $this.data('qid');
        ctx['action'] = action;
        ctx['id'] = id;
    $.ajax('/vote/', {
        method: 'POST',
        data: ctx,
    }).done(function(data) {
        if (ctx['like'] == 'question')
            $('#like-question-rating-' + id).text(data.likes);
        else if (ctx['like'] == 'answer')
            $('#like-answer-rating-' + id).text(data.likes);
    });
    console.log("HERE " + action + " " + id);
});