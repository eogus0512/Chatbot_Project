$('.send').click(function(){
    var message = $('.message').val();
    
    var postdata = {
        'query':message
    }
    appendMessageTag("right", "USER", postdata['query']);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/query/TEST',
        data: JSON.stringify(postdata),
        dataType : 'JSON',
        contentType: "application/json",
        success: function(ret){
            appendMessageTag("left", "Chatbot", ret['Answer'])
        },
        error: function(request, status, error){
            alert('통신 실패')
            alert(error);
        }
     })
    $('.message').val('');
})

$(document).on('keydown', 'div.input input', function(e){
    if(e.keyCode == 13 && !e.shiftKey) {
        e.preventDefault();
        var message = $('.message').val();
        
        var postdata = {
            'query':message
        }
        appendMessageTag("right", "USER", postdata['query']);
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/query/TEST',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(ret){
                appendMessageTag("left", "Chatbot", ret['Answer'])
            },
            error: function(request, status, error){
                alert('통신 실패')
                alert(error);
            }
        })
        $('.message').val('');
    }
})


function createMessageTag(LR_className, senderName, message) {
    let chatLi = $('div.chatFormat ul li').clone();

    chatLi.addClass(LR_className);
    chatLi.find('.sender span').text(senderName);
    chatLi.find('.intent span').text(message);

    return chatLi;
}

function appendMessageTag(LR_className, senderName, message) {
    const chatLi = createMessageTag(LR_className, senderName, message);

    $('div.chat ul').append(chatLi);
    $('div.chat').scrollTop($('div.chat').prop('scrollHeight'));
}
