$(document).ready(function() {
    $("textarea").val('');

    // like a post
    $(".like").click(function() {
        
        var post_id = $(this).attr('id');
        var url = "/post/" + post_id + "/like";
        $.get($SCRIPT_ROOT + url, 
        function(data, success) {
            // alert(data.result + " \nstatus: " + success);
            var likeId = "#like-" + post_id;
            var olddata = $(likeId).text();
            $(likeId).text(data.result);
            
            // update like icon
            if(data.result > olddata) {
                $('#' + post_id).addClass("liked");
                $('#' + post_id).html("<i class='fas fa-heart'></i>");
            }
            else {
                $('#' + post_id).removeClass("liked");
                $('#' + post_id).html("<i class='far fa-heart'></i>");
            }
        });
    });

    // post new comment
    $(".post-comment").click(function() {
            
        var post_id = $(this).attr('id');
        var msg = $("#comment-on-" + post_id).val();

        // alert('comment ' + msg);
        msg = $.trim(msg);
        // aler(msg);
        // return;
        if(msg == '') {
            alert("Cannot post empty comment");
            return false;
        }
        var url = "/comment/" + post_id;
        $.post($SCRIPT_ROOT + url,
        {
            msg: msg
        },
        function(data, success) {
            //alert(data.content + '\n ' + success);
            $("#comment-on-" + post_id).val('');

            var comment = "<span class='comment'><a class='text-dark user-link' href='" 
                + data.user_url + "'>" + data.username + "</a> " + data.content + "</span>";

            $("#comments-on-" + post_id).append(comment);
        });
    });

    // delete a comment 
    $(".delete-comment").click(function(e) {
        e.preventDefault();

        var com_id = $(this).attr('id').split('-')[1];
        var url = "/comment/" + com_id + "/delete";

        $.get($SCRIPT_ROOT + url, 
        function(data, success) {
            // alert('deleted');
            $("#c" + com_id).remove();
        });
    });
});