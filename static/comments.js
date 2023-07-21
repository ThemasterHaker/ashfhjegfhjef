const commentPostBtn = document.getElementById("comment")
const closeCommentBtn = document.getElementById("comment-cancel")

function openComment() {
    document.querySelector(".comment-popup").style.display = "flex"
    commentPostBtn.style.display = "none"

}

function closeComment() {
    document.querySelector(".comment-popup").style.display = "none"
    commentPostBtn.style.display = "inline-block"
}


commentPostBtn.addEventListener("click", openComment)
closeCommentBtn.addEventListener("click", closeComment)