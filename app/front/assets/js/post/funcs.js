function savePost() {

    let h = new Headers()
    h.append("Authorization", JWT)

    
    let fd = new FormData()
    let imgs = document.getElementById("new_post_images")
    let cont = document.getElementById("new_post_content")
    let prof = document.getElementById("new_post_profile")
    let priv = document.getElementById("new_post_privacity")

    let is_profile = false

    if (cont.value) { fd.append("content", cont.value) }
    if ( prof ){ 
        if (prof.checked) {
            fd.append("profile", prof.checked)
            is_profile = prof.checked
        }
    }

    fd.append("privacity", priv.value )

    Array.from(imgs.files).forEach(f => { fd.append("images", f) })
    let init = {
        method:"POST",
        headers:h,
        mode: "cors",
        body: fd
    }
    if(fd.get("images") || fd.get("content")){
        fetch( URL_post_post, init)
        .then( response => response.json())
        .then( data => {
            if( prof ){ prof.checked = "" }
            cont.value = ""
            imgs.type = "text"
            imgs.type = "file"
            
            document.getElementById("new_post_preview").innerHTML = ""
            setPostUI(data)
            if( is_profile ) {
                let divs = document.getElementsByClassName("user_profile_"+ currentUser.id)
                Array.from( divs ).forEach(elem => { elem.src = data.user.profile.img.url })
            }
        })
        .catch( (error) => {console.log(error) })
    }
    return
}

function share(post) {
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch(URL_post_post, {method:"post", headers:h, body: JSON.stringify({shared: post, privacity: "public"}) })
    .then( response => response.json())
    .then( data => {
        setPostUI(data)
        let sh = document.getElementsByClassName("shares_"+data.shared.id)
        Array.from(sh).forEach(btn => { btn.innerText = data.shared.count })
    })
    .catch( (error) => {console.log(error) })
    return
}

function update_post() {
    let editArea = document.getElementById("edit_post")
    if( editArea ){
        
        let content = editArea.getElementsByClassName("content")[0]
        let privacity = editArea.getElementsByClassName("privacity")[0]
        let delPictures = editArea.getElementsByClassName("pictures_deleted")[0] 
        let newPictures = editArea.getElementsByClassName("edit_newImages")[0]
        let oldPictures = editArea.getElementsByClassName("pictures")[0]
        oldPictures = get_json_data(oldPictures.getAttribute("data"))

        if( ! newPictures ){
            let newPictures = document.createElement("input")
            newPictures.type = "file"
        }

        if(content.value || newPictures.files.length || oldPictures ) {
            
            let h = new Headers()
            h.append("Authorization", JWT)
            
            let fd = new FormData()
            fd.append("content", content.value) 
            if( privacity.value ) { fd.append("privacity", privacity.value) }
            if( delPictures.value ) { fd.append("delete", delPictures.value) }
            if( newPictures.files.length ) {  Array.from(newPictures.files).forEach( f => { fd.append("images", f) } ) }


            fetch(URL_post + editArea.getAttribute("data"),{
                headers: h,
                method: "put",
                body: fd
            })
            .then( response => response.json() )
            .then( data => {
                let  post = document.getElementById(data.id)
                post.innerHTML = create_post(data).outerHTML
                post.setAttribute("data", set_json_data(data))
                editArea.remove()
            })
            .catch( error => { console.log(error) })
            return
        }
    }
}

function del_post(post) {
    let h = new Headers({Authorization: JWT})

    fetch(URL_post + post,{
        method: "delete",
        headers: h
    })
    .then( response => {
        Array.from(document.getElementsByClassName("shared_"+post)).forEach(
            p => {
                let p_p = p.getElementsByClassName("pictures")[0]
                let p_l = p.getElementsByClassName("legend")[0]

                let btnDel = p.getElementsByClassName("btn_del_post")[0]
                let btnEdit = p.getElementsByClassName("btn_edit_post")[0]

                btnEdit.remove()
                btnDel.remove()

                p_p.remove()
                p_l.remove()

                let sh_p = document.createElement("p")
                sh_p.textContent = "O post original foi excluido pelo usuario!"
                p.appendChild(sh_p)
            }
        )
        document.getElementById(post).remove()
    })
    .catch( (error) => { console.log(error) })
    return
}


function set_friend( user ) {
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch( URL_friends_post, {
        method: "post",
        headers: h,
        body: JSON.stringify({ user: user })
    })
    .then( response => {
        let btns = document.getElementsByClassName(`btn_friend_${user}`)
        Array.from(btns).forEach(
            btn => {
                btn.textContent = "Cancelar Solicitação de Amizade"
                btn.setAttribute("onclick", `del_friend('${user}')`)
            }
        )    
    })
    .catch( error => {console.log( error ) })
}

function accept_friend( user ) {
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch( URL_friends_post,{
        method: "put",
        data: JSON.stringify({ user: user })
    })
    .then( response => {
        let btns = document.getElementsByClassName(`btn_friend_${user}`)
        Array.from(btns).forEach(
            btn => {
                btn.textContent = "Desfazer Amizade"
                btn.setAttribute("onclick", `del_friend('${user}')`)
            }
        )    
    })
    .catch( error => {console.log( error ) })
}

function del_friend( user ) {
    let h = new Headers({Authorization: JWT})

    let init = {
        method: "delete",
        headers: h,
        body: { user: user}
    }

    fetch(URL_friends_post, init)
    .then( response => response.json() )
    .then( data => {
        let btns = document.getElementsByClassName(`btn_friend_${user}`)
        Array.from(btns).forEach(
            btn => {
                btn.textContent = "Enviar Solicitação de Amizade"
                btn.setAttribute("onclick", `set_friend('${user}')`)
            }
        )    
    })
    .catch( error => {console.log( error ) })
}


function loadPosts() {

    loadUserData
    .then( function(){
        create_new_post_form()
        let h = new Headers({Authorization:JWT})
        
        fetch( URL_post_get_list,{headers: h} )
        .then( response => response.json() )
        .then( data => { data.posts.forEach(element => {  setPostUI(element) }) })
        .catch((error) => { console.log(error) })

    })
    .catch( error => { console.log( error ) } )
    
}
