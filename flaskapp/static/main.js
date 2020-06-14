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

    document.querySelector('.share').onclick = link_share;

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


// article template
function template(post) {

    let liked = '';
    let icon = 'r';

    if(post.liked == true) {
        // console.log(post.pid, 'liked');
        liked = 'd';
        icon = 's';
    }
    
    let content = `<div class="card article">
            <div class="card-header">
                <img  class="account-img rounded-circle" src="${post.author.image_file}">
                <a class="text-dark user-link" href="${post.author.user_url}">${post.author.username}</a>
            </div>
    
                <div class="main-img-wrapper bg-light">
                    <img src="${post.media}" class="card-img-top post-media rounded-0" alt="">
                </div>

            <div class="card-body pb-2">
                <div class="card-text post-meta-data">
                    <span id="l-${post.pid}" class="up-info like${liked}"><i class='fa${icon} fa-heart'></i></span>

                    <span class="up-info">
                        <a class="text-dark" href="${post.post_url}"><i class="far fa-comment"></i></a>
                    </span>
                    <span id="sh-${post.pid}" class="up-info"><i class="fa fa-share"></i></span>
                    
                    
                    <small class=""><a class="float-right text-muted" href="${post.post_url}">View</a></small>

                    <div class="like-counter">
                        <span id="like-${post.pid}" class="like-count">${post.like_count}</span>
                        likes
                    </div>
            
                </div>`;
                if(post.content.length > 0 ) {
                    content = content + 
                    `<span class="card-text"> 
                            <a class="text-dark user-link " href="${post.author.user_url}">${post.author.username}</a>
                            ${post.content}
                    </span>`;
                }
                content = content + 
                `<div class="comments" id="comments-on-${post.pid}">`;
                    if (post.comment_count > 2) {
                        content = content + 
                        `<a class="text-muted" href="${post.post_url}">View all ${post.comment_count} comments</a>`;
                    }
                    post.comments.forEach(comment => {
                        content = content + 
                        `<span class="comment" id="c${comment.cid }">
                        <a class="text-dark user-link" href="${comment.author.user_url}">${comment.author.username}</a>
                            ${comment.content}
                        </span>`
                    });
                content = content + `</div>
                <small class="text-muted text-uppercase">${post.timeago}</small>
            </div>

            <div class="modal-footer home-comment-box">
                <ul class="list-group list-group-flush" style="width: 85%;">
                    <textarea class="text-muted comment-box make-comment" id="comment-on-${post.pid}" placeholder="Add a comment.."></textarea>
                </ul>
                <button class="btn post-comment" id="c-${post.pid}">Post</button>
        </div>
    </div>`;

    return content;
};


// explore post template
function explore_template(post) {

    let content = `<div class="col p-2 img-wrapper rounded">
                    <a href="${post.post_url}"><img class="post-img" src="${post.media}"></a>
            </div>
    </div>`;

    return content;
};


function link_share() {
    const pid = this.id.split('-')[1];
    const link = window.location.host + $SCRIPT_ROOT + '/post/id/' + pid;
    
    var dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = link;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);

    alert("Link copied: " + link);
}