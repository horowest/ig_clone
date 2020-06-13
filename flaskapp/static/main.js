// handle comments 
function comment_handler() {
                        
    var post_id = $(this).attr('id').split('-')[1];
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

        var comment = "<span class='comment' id='c" + data.cid + "'><a class='text-dark user-link' href='" 
            + data.user_url + "'>" + data.username + "</a> " + data.content 
            + "<small class='float-right delete-comment' id='comment-" + data.cid 
            + "'><a class='text-danger' href='#'>delete</a></small>"
            + "</span>";

        $("#comments-on-" + post_id).append(comment);
        $("#c-" + post_id).attr("disabled", true);

        $('#comment-' + data.cid).click(function(e) {
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
}

// enable or diable post button
function enable_disable_button() {
    const com_id = this.id.split('-')[2];
    let com = this.value;

    if (com.length > 0)
        document.querySelector(`#c-${com_id}`).disabled = false;
    else 
        document.querySelector(`#c-${com_id}`).disabled = true;
}


// like a post
function like_post() {
    var post_id = $(this).attr('id').split('-')[1];
    var url = "/post/" + post_id + "/like";
    $.get($SCRIPT_ROOT + url, 
    function(data, success) {
        // alert(data.result + " \nstatus: " + success);
        var likeId = "#like-" + post_id;
        var olddata = $(likeId).text();
        $(likeId).text(data.result);
        
        // update like icon
        if(data.result > olddata) {
            $('#l-' + post_id).addClass("liked");
            $('#l-' + post_id).html("<i class='fas fa-heart'></i>");
        }
        else {
            $('#l-' + post_id).removeClass("liked");
            $('#l-' + post_id).html("<i class='far fa-heart'></i>");
        }
    });
}


// delete comment
function delete_comment(e) {
    e.preventDefault();

    var com_id = $(this).attr('id').split('-')[1];
    var url = "/comment/" + com_id + "/delete";

    $.get($SCRIPT_ROOT + url, 
    function(data, success) {
        // alert('deleted');
        $("#c" + com_id).remove();
    });
}


$(document).ready(function() {

    $('.post-comment').attr("disabled", true);

    $('.make-comment').on('keyup', enable_disable_button);

    // follow user
    $("#flw").click(function() {
        var t = $("#flw").text();
        if(t == "Follow") {
            $.post($SCRIPT_ROOT + "/follow", 
            { 
                username: $("#user").text() 
            }, 
            function(data, success) {
                // alert(data.result + " status: " + success);
                $("#flw").text('Following');
                $("#flw").removeClass('btn-primary');
                $("#flw").addClass('btn-secondary');
            });
        }
        else if(t == "Following") {
            $.post($SCRIPT_ROOT + "/unfollow", 
            { 
                username: $("#user").text() 
            }, 
            function(data, success) {
                // alert(data.result + " status: " + success);
                $("#flw").text('Follow');
                $("#flw").removeClass('btn-secondary');
                $("#flw").addClass('btn-primary');
            });
        }
    }); 


    // follow suggs users
    $(".flw-sug").click(function(e) {
        e.preventDefault();

        let user_id = $(this).attr('id').split('-')[1];
        let follows_or_not = $(this).text();
        let username = $("#flw-"+user_id).text().trim();

        console.log(username);
        console.log(follows_or_not);

        if(follows_or_not == 'Follow') {
            // alert('to follow');
            $.post($SCRIPT_ROOT + "/follow",
            { 
                username: username
            },
            function(data, success) {
                // alert(data.result + " status: " + success);
                $('#s-'+user_id).text('Following');
                $('#s-'+user_id).removeClass('text-primary');
                $('#s-'+user_id).addClass('text-secondary');
            });
        }
        else if(follows_or_not == 'Following') {
            // alert('to follow');
            $.post($SCRIPT_ROOT + "/unfollow",
            { 
                username: username
            },
            function(data, success) {
                // alert(data.result + " status: " + success);
                $('#s-'+user_id).text('Follow');
                $('#s-'+user_id).removeClass('text-secondary');
                $('#s-'+user_id).addClass('text-primary');
            });
        }

    });


    $("textarea").val('');

    // like a post
    $(".like").click(like_post);

    // post new comment
    $(".post-comment").click(comment_handler);

    // delete a comment 
    $(".delete-comment").click(delete_comment);
});