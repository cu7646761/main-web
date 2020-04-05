


let btnSubmitComment = document.getElementById("commento-submit-button-root")

btnSubmitComment.addEventListener("click", e => {
    let author = document.getElementById("commento-markdown-button-root");
    let commentContent = document.getElementById("commento-textarea-root");
    console.log(author.value)
    let authorName = author.value == "" ? "Anonymous" : author.value;

    let newComment = `
    <div class="commento-comments">
                                    <div>
                                        <div id="commento-comment-card" class="commento-card" style="border-left: 2px solid rgb(146, 36, 40);">
                                            <div class="commento-header">
                                                <div class="commento-avatar" style="background: rgb(146, 36, 40);">
                                                    Hdawmdmakwdmkawmd
                                                </div>
                                                <div id="commento-comment-name" class="commento-name" style="max-width: 98px;">${authorName}</div>
                                                <div id="commento-comment-subtitle" class="commento-subtitle">
                                                    <div id="commento-comment-timeago" title="Thu Oct 24 2019 14:37:16 GMT+0700 (Indochina Time)" class="commento-timeago">1 hours ago</div>
                                                </div>
                                            </div>
                                            <div id="commento-comment-contents">
                                                <div id="commento-comment-body" class="commento-body">
                                                    <div id="commento-comment-text">
                                                        <p>${commentContent.value}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
    `

    let commentsSection = document.getElementById("commento-main-area")

    commentsSection.insertAdjacentHTML('beforeend', newComment)

    let postId = document.getElementById("post-title-id").dataset.postId

    let COMMENT_API = `https://original-glider-246113.appspot.com/posts/${postId}/comments`

    var xhr = new XMLHttpRequest();
    xhr.open("POST", COMMENT_API, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        author_name: author.value,
        content: commentContent.value,
    }));

    author.value = "";
    commentContent.value = "";
})


let showComments = async () => {
    let postId = document.getElementById("post-title-id").dataset.postId

    let COMMENT_API = `https://original-glider-246113.appspot.com/posts/${postId}/comments`
    let res = await fetch(COMMENT_API)

    let data = await res.json()

    comments = data.data;

    for (let ci = 0; ci < comments.length; ci++) {
        const comment = comments[ci];

        let newComment = `
        <div class="commento-comments">
                                        <div>
                                            <div id="commento-comment-card" class="commento-card" style="border-left: 2px solid rgb(146, 36, 40);">
                                                <div class="commento-header">
                                                    <div class="commento-avatar" style="background: rgb(146, 36, 40);">
                                                        Hdawmdmakwdmkawmd
                                                    </div>
                                                    <div id="commento-comment-name" class="commento-name" style="max-width: 98px;">${comment.author}</div>
                                                    <div id="commento-comment-subtitle" class="commento-subtitle">
                                                        <div id="commento-comment-timeago" title="Thu Oct 24 2019 14:37:16 GMT+0700 (Indochina Time)" class="commento-timeago">1 hours ago</div>
                                                    </div>
                                                </div>
                                                <div id="commento-comment-contents">
                                                    <div id="commento-comment-body" class="commento-body">
                                                        <div id="commento-comment-text">
                                                            <p>${comment.content}</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
        `

        let commentsSection = document.getElementById("commento-main-area")

        commentsSection.insertAdjacentHTML('beforeend', newComment)

    }


}

showComments()