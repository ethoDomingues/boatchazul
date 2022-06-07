
function setComment(formId) {
    
    let form = document.getElementById(formId)
    
    let img = form.getElementsByClassName("comm_image")[0]
    let owner = form.getElementsByClassName("comm_owner")[0]
    let content = form.getElementsByClassName("comm_text")[0]
    let counter = form.getElementsByClassName("comms_counter")[0]
    
    
    if( content.value || img.value ) {
        let h = new Headers()
        h.append("Authorization", JWT)

        let fd = new FormData()
        fd.append("owner", owner.value)

        if( content.value ) { fd.append("content", content.value) }
        if( img.files ) { fd.append("image", img.files[0]) }
        
        fetch(URL_comments_post,{ method:"post", headers:h, body: fd })
        .then( response => response.json() )
        .then( data => {
            content.value = ""
            img.type = "text"
            img.type = "file"
            
            counter.innerHTML = data.comments.length
            
            post = document.getElementById(form.getAttribute("postid"))
            comments_area = post.getElementsByClassName("comments")
            if (comments_area.length) {
                comments_area[0].insertAdjacentElement("afterBegin", create_comment(data.new_comment))
            } else {
                wrapperComm = post.getElementsByClassName("wrapper_comments_area")[0]
                wrapperComm.replaceChildren(create_comments_area(data))
            }
        })
        .catch( (error) => {console.log(error) })
    }
    return
}


function del_comm(comm) {
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch( URL_comments + `${comm}`,{ method: "delete", headers: h })
    .then( response => response.json() )
    .then( data => {
        let post = document.getElementById(data.id)
        post.getElementsByClassName("comms_counter")[0].innerText = data.count
        document.getElementById(comm).remove()
        if( data.count == 0 ){ post.getElementsByClassName("comments")[0].remove() }
    })
    .catch( (error) => { console.log(error) })
    return null
}


function react(owner) {
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')
    
    fetch( URL_reacts_post + owner, {method: "post", headers:h} )
    .then( response => response.json())
    .then( data => {
        r = document.getElementsByClassName("reacts_"+owner)[0]
        if(data.reacts.includes(currentUser.id)){
            r.textContent = `Descurtir ${data.reacts.length}`
        } else {
            r.textContent = `Curtir ${data.reacts.length}`
        }
    })
    .catch((error) => { console.log(error) })
}