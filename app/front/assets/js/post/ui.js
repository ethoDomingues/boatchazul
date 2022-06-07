

function setPostUI(data) {
    let render = false
    let privacity = data.privacity
    
    if( data.user.id == currentUser.id ) {
        render = true
    } else if( privacity == "public" ){
        render = true
    } else if( privacity == "friends" ){
        if(currentUser.friends.ids.includes(data.user.id)){
            render = true
        }
    } else if( privacity.members ){
        if(privacity.members.ids.includes(currentUser.id)){
            render = true
        }
    }

    if(render){
        let newPost = create_post(data)
        document.getElementById("posts").insertAdjacentElement("afterBegin", newPost)
    }
    return
}


function create_new_post_form() {

    let content = document.createElement("textarea")
    let content_wrapper = document.createElement("div")

    content_wrapper.appendChild(content)

    let images = document.createElement("input")
    let images_label = document.createElement("label")
    let images_wrapper = document.createElement("div")

    images_wrapper.appendChild(images_label)
    images_wrapper.appendChild(images)

    let profile = document.createElement("input")
    let profile_label = document.createElement("label")
    let profile_wrapper = document.createElement("div")

    profile_wrapper.appendChild(profile)
    profile_wrapper.appendChild(profile_label)

    let privacity = document.createElement("select")
    let privacity_label = document.createElement("span")
    let privacity_wrapper = document.createElement("div")

    privacity_wrapper.appendChild(privacity_label)
    privacity_wrapper.appendChild(privacity)

    let btnSave = document.createElement("button")

    content.classList.add("new_post_content")
    content.setAttribute("id","new_post_content")
    content.setAttribute("placeholder","Eae fio, qual a a boa?")

    
    images.type = "file"
    images.hidden = true
    images.classList.add("new_post_images")
    images.setAttribute("id","new_post_images")
    images.setAttribute("onchange","new_post_preview()")
    images.setAttribute("multiple","")

    images_label.setAttribute("for","new_post_images")
    images_label.textContent = "Add Image"



    profile.type = "checkbox"
    profile.setAttribute("id","new_post_profile")
    profile.classList.add("new_post_profile")

    profile_label.textContent = "Perfil"
    profile_label.setAttribute("for", "new_post_profile")


    privacity.setAttribute("id","new_post_privacity")
    privacity_label.textContent = "Privacidade"
    if( currentGroup.id ){
        let opt = document.createElement("option")
        opt.value = currentGroup.id
        opt.textContent = currentGroup.name
        opt.selected = true
        privacity.appendChild( opt )
        privacity_wrapper.hidden = true
    } else {
        let optPublic = document.createElement("option")
        let optFriends = document.createElement("option")

        optPublic.value = "public"
        optPublic.textContent = "Público"
        privacity.appendChild(optPublic)
        
        optFriends.value = "friends"
        optFriends.textContent = "Amigos"
        privacity.appendChild(optFriends)

        if( currentUser.groups.ids.length ){
            currentUser.groups.groups.forEach(g => {
                let opt = document.createElement("option")
                opt.value = g.id
                opt.textContent = g.name
                privacity.appendChild(opt)
            })
        }
    }



    btnSave.setAttribute("onclick","savePost()")
    btnSave.textContent = "Publicar"

    let div = document.getElementById("new_post")

    div.appendChild(content_wrapper)
    div.appendChild(images_wrapper)
    if(! currentGroup.id ){ div.appendChild(profile_wrapper) }
    div.appendChild(privacity_wrapper)
    div.appendChild(btnSave)

    return 
}

function create_post( data ) {
    let newPost = document.createElement("article")
    newPost.classList.add("posts")
    newPost.setAttribute("id", data.id)
    newPost.setAttribute("data", set_json_data(data))

    newPost.appendChild(create_userarea_element(data))
    newPost.appendChild(create_content(data))
    newPost.appendChild(create_button_area_bottom(data))
    newPost.appendChild(create_comments_area(data))

    return newPost
}

function create_content( data ) {
    let content = document.createElement("div")
    let legend = document.createElement("div")
    let pics = document.createElement("div")    
    
    content.classList.add("content")
    legend.classList.add("legend")
    

    if( data.content ){ legend.textContent = data.content }
    if( data.shared ) { pics = create_shared_content(data.shared) }
    else if( data.pictures ){    
        pics.classList.add("pictures")
        data.pictures.forEach(element => { pics.appendChild( create_image(element) ) })
    }

    if( data.content ){ content.appendChild(legend) }
    if( data.pictures.length || data.shared ){ content.appendChild(pics) }
    return content
}

function create_shared_content(data) {


    let div = document.createElement("div")
    let pics = document.createElement("div")
    let cont = document.createElement("div")
    
    div.classList.add("shared_content")
    pics.classList.add("pictures")
    cont.classList.add("legend")


    if( data.content ){
        cont = document.createElement("p")
        cont.classList.add("legend")
        cont.textContent = data.content
    }
    
    if( data.pictures ){
        data.pictures.forEach(image => { pics.appendChild(create_image(image)) })        
    }
    
    div.classList.add(`shared_${data.id}`)
    div.style.padding = "10px"
    div.appendChild(create_userarea_element(data))

    
    if( data.deleted ){
        if(data.user.id == currentUser.id){ cont.textContent = "Esse post foi excluido por vocẽ!"}
        else { cont.textContent = "O post original foi excluido pelo usuario!" }
        
        div.appendChild(cont)
    }
    else {
        div.appendChild(cont)
        div.appendChild(pics)
    }

    return div
}

function create_userarea_element( data ) {

    let img_profile = new Image()
    let userArea = document.createElement("div")
    let username = document.createElement("p")
    
    img_profile.classList.add("user_profile")
    
    if(data.user.profile){
        img_profile.src = data.user.profile.img.url
    } else if(data.user.all_profile){
        data.user.all_profile.forEach(prof => { if( prof.active ){ img_profile.src = prof.img.url } })
    }

    else { img_profile.src = "/assets/img/batata.jpg" }

    img_profile.classList.add(`user_profile_${data.user.id}`)
    img_profile.style.width = "30px"

    userArea.classList.add("user_area")
    userArea.appendChild(img_profile)

    username.style.color = "#fff"
    username.textContent = " @" + data.user.username

    userArea.appendChild(username)
    
    if(data.user.id == currentUser.id && ! data.deleted ){
        let btnDeletePost = document.createElement("button")
        let btnEditPost = document.createElement("button")
        let obj = data.id.split("@")[0]
        
        btnDeletePost.classList.add("btn_del_post")
        btnDeletePost.textContent = "Excluir"

        btnEditPost.classList.add("btn_edit_post")
        btnEditPost.textContent = "Editar"
        
        if( obj == "posts" ){
            btnDeletePost.setAttribute("onclick", `del_post('${data.id}')`)
            btnEditPost.setAttribute("onclick", `edit_post_ui('${data.id}')`)
        } else if( obj == "comments" ) {
            btnDeletePost.setAttribute("onclick", `del_comm('${data.id}')`)
            btnEditPost.setAttribute("disabled", '')
        }
        btnDeletePost.style.margin = "5px"

        userArea.appendChild(btnDeletePost)
        userArea.appendChild(btnEditPost)



    } else if(data.user.id != currentUser.id){
        
        if( currentUser.friends.ids.includes(data.user.id) ) {
            let btnFriend = document.createElement("button")
            btnFriend.classList.add(`btn_friend_${data.user.id}`)
            btnFriend.textContent = "Desfazer Amizade"
            btnFriend.style.margin = "5px"

            btnFriend.setAttribute("onclick", `del_friend('${data.user.id}')`)

            userArea.appendChild(btnFriend)

        } else if( currentUser.solicitations.received.ids.includes(data.user.id) ){

            let btnFriend = document.createElement("button")
            btnFriend.classList.add(`btn_friend_${data.user.id}`)
            btnFriend.textContent = "Aceitar Solicitação de Amizade"
            btnFriend.style.margin = "5px"

            btnFriend.setAttribute("onclick", `accept_friend('${data.user.id}')`)

            userArea.appendChild(btnFriend)

        } else if( currentUser.solicitations.sender.ids.includes(data.user.id) ){

            let btnFriend = document.createElement("button")
            btnFriend.classList.add(`btn_friend_${data.user.id}`)
            btnFriend.textContent = "Cancelar Solicitação de Amizade"
            btnFriend.style.margin = "5px"

            btnFriend.setAttribute("onclick", `del_friend('${data.user.id}')`)

            userArea.appendChild(btnFriend)


        } else { 
            let btnFriend = document.createElement("button")
            btnFriend.classList.add(`btn_friend_${data.user.id}`)
            btnFriend.textContent = "Enviar Solicitação de Amizade"
            btnFriend.style.margin = "5px"

            btnFriend.setAttribute("onclick", `set_friend('${data.user.id}')`)

            userArea.appendChild(btnFriend)
        }
    }
    if( data.privacity ){
        let privac = document.createElement("sub")
        if( data.privacity.id ){
            privac.textContent = " >>> " + data.privacity.name
        } else {
            privac.textContent = " >>> " + data.privacity
        }
        userArea.appendChild(privac)
    }


    return userArea
}

function create_button_area_bottom( data ){

    btnReact = document.createElement("button")
    btnReact.setAttribute("onclick",`react('${data.id}')`)
    btnReact.classList.add(`reacts_${data.id}`)
    if(data.reacts.includes(currentUser.id)){
        btnReact.textContent = `Descurtir ${data.reacts.length}`
    } else {
        btnReact.textContent = `Curtir ${data.reacts.length}`
    }
    

    let btnShare = document.createElement("button")
    btnShare.setAttribute("onclick",`share('${data.id}')`)
    btnShare.textContent = "Share "
       


    let div = document.createElement("div")
    div.classList.add("button_area_bottom")
    div.style.display = "flex"
    div.style.alignItems = "center" 
    div.style.justifyContent = "space-around"

    div.appendChild(btnReact)
    div.appendChild(btnShare)

    return div
}

function create_comments_area( data ) {
    let comm_text = document.createElement("textarea")
    let comm_image = document.createElement("input")
    let comm_counter = document.createElement("span")
    let comm_owner = document.createElement("input")
    let comm_form = document.createElement("div")
    let comms = document.createElement("div")

    let btnSave = document.createElement("button")
    let wrapper = document.createElement("div")
    
    
    comm_text.setAttribute("placeholder","Escreva aqui")
    comm_text.name = "comm_text"
    comm_text.classList.add("comm_text")

    comm_image.type = "file"
    comm_image.name = "comm_image"
    comm_image.classList.add("comm_image")

    comm_owner.type = "hidden"
    comm_owner.value = data.id
    comm_owner.name = "comm_owner"
    comm_owner.classList.add("comm_owner")

    comm_counter.classList.add("comms_counter")
    comm_counter.textContent = data.comments.length

    btnSave.setAttribute("onclick", `setComment('comm_form_${data.id}')`)
    btnSave.textContent = "Comentários - "
    btnSave.appendChild(comm_counter)

    comm_form.setAttribute("id","comm_form_"+data.id)
    comm_form.setAttribute("postID",data.id)
    comm_form.style.width="500px"
    comm_form.style.heigth="200px"

    comm_form.appendChild(comm_text)
    comm_form.appendChild(comm_image)
    comm_form.appendChild(comm_owner)
    comm_form.appendChild(btnSave)

    comms.classList.add("comments")

    data.comments.forEach( comm => { comms.appendChild(create_comment(comm)) })

    wrapper.classList.add("wrapper_comments_area")
    wrapper.appendChild(comm_form)
    if( data.comments.length ){ wrapper.appendChild(comms) }
    return wrapper
}

function create_comment( comm ) {
    let content = document.createElement("div")
    let picture = document.createElement("div")
    let comment = document.createElement("div")
    content.classList.add("comm_text")
    picture.classList.add("comm_picture")


    if( comm.content ){ content.textContent = comm.content }
    if( comm.picture ){ picture.appendChild( create_image(comm.picture) ) }

    comment.setAttribute("id", comm.id)
    comment.classList.add("comm_content")

    comment.appendChild(create_userarea_element(comm))
    comment.appendChild(content)

    btnReact = document.createElement("button")
    btnReact.setAttribute("onclick",`react('${comm.id}')`)
    btnReact.classList.add(`reacts_${comm.id}`)
    if(comm.reacts.includes(currentUser.id)){
        btnReact.textContent = `Descurtir ${comm.reacts.length}`
    } else {
        btnReact.textContent = `Curtir ${comm.reacts.length}`
    }

    comment.appendChild(btnReact)

    if( comm.picture ){ comment.appendChild(picture) }
    return comment
}

function create_image( data ) {
    let img = new Image()
    img.src = data.url
    img.setAttribute("id",data.id)
    img.style.width = "200px"
    img.classList.add("picture")
    return img
}

function create_wrapper_img( data, is_profile=null ){
    let wrapper_img = document.createElement("div")
    wrapper_img.setAttribute("id",`edit_img_${data.id}`)
    wrapper_img.setAttribute("data",`${data.id}`)
    wrapper_img.style.border = "1px solid #28b700"
    

    if( is_profile ){
        wrapper_img.style.border = "1px solid #00f"
    } else {
        let delBtn = document.createElement("button")
        delBtn.classList.add("btn_wrapper_img")
        delBtn.textContent = "Excluir"
        delBtn.setAttribute("onclick", `edit_popImg('edit_img_${data.id}')`)
        wrapper_img.appendChild(delBtn)
    }
    wrapper_img.appendChild(create_image(data))
    return wrapper_img
}



function edit_post_ui( postid ) {

    let edit_post = document.getElementById("edit_post")
    let conf = true
    if( edit_post ){
        conf = confirm("Vc deseja cancelar esta edição?")
        if( conf ) { edit_post.remove() }
    }

    
    if( postid && conf ) {
        fetch(URL_post + postid )
        .then( response => response.json() )
        .then( data => {
            let is_profile = Boolean(data.profile)

            let privacityLabel = document.createElement("span")
            privacityLabel.textContent = "Privacidade"

            let privacity = document.createElement("select")
            privacity.setAttribute("id", "edit_privacity")
            privacity.setAttribute("name", "privacity")
            privacity.classList.add("privacity")
            if(data.privacity.id){privacity.disabled = true}

            if( data.privacity.id ) {
                let opt = document.createElement("option")
                opt.textContent = data.privacity.name
                privacity.appendChild(opt)
            } else {
                let opts = {public: "Público", friends: "Amigos"}
                Object.keys(opts).forEach( priv => {
                    let opt = document.createElement("option")
                    opt.value = priv
                    opt.textContent = opts[priv]
                    privacity.appendChild(opt)
                })
                
            }
            

            let legend = document.createElement("textarea")
            legend.value = data.content
            legend.classList.add("content")
            legend.style.width = "90%"
            legend.style.padding = "10px"
            legend.style.margin = "10px 2%"

            legend.setAttribute("placeholder", "Escreva uma legenda.")
            
            let pic_ids = []

            let pictures = document.createElement("div")
            pictures.classList.add("pictures")

            data.pictures.forEach(img => {
                pic_ids.push(img.id)
                pictures.appendChild(create_wrapper_img(img, is_profile))
            })
            pictures.setAttribute("data", set_json_data(pic_ids))

            let new_pictures_wrapper = document.createElement("div")
            let new_pictures = document.createElement("input")
            let new_pictures_label = document.createElement("label")
            let np_counter = document.createElement("span")

            new_pictures.type = "file"
            new_pictures.name = "images"
            new_pictures.classList.add("edit_newImages")
            new_pictures.setAttribute("id", "edit_newImages" )
            new_pictures.setAttribute("onchange", "edit_imagePreview()" )
            new_pictures.setAttribute("multiple","")
            new_pictures.style.display = "none"
            
            new_pictures_label.classList.add("edit_new_pictures_label")
            new_pictures_label.setAttribute("for", "edit_newImages" )
            new_pictures_label.textContent = "Add Mídia"
            
            np_counter.classList.add("new_picture_counter")
            np_counter.textContent = "0"
            
            
            new_pictures_label.appendChild(np_counter)
            
            new_pictures_wrapper.appendChild(new_pictures)
            new_pictures_wrapper.appendChild(new_pictures_label)

            if( is_profile ){ new_pictures_wrapper.hidden = true }

            let _pics_deleted = document.createElement("input")
            _pics_deleted.classList.add("pictures_deleted")
            _pics_deleted.name = "deleted"
            _pics_deleted.type = "hidden"


            let btnSave = document.createElement("button")
            btnSave.classList.add("edit_post")
            btnSave.textContent = "Salvar"
            btnSave.setAttribute("onclick", `update_post('${data.id}')`)


            let btnCancel = document.createElement("button")
            btnCancel.classList.add("cancel")
            btnCancel.textContent = "Cancelar"
            btnCancel.setAttribute("onclick", `edit_cancel()`)


            let edit_area = document.createElement("div")
            edit_area.setAttribute("id", "edit_post")
            edit_area.setAttribute("data", postid)
            edit_area.style.background = "#444"

            edit_area.appendChild(btnSave)
            edit_area.appendChild(btnCancel)
            edit_area.appendChild(document.createElement("br"))

            edit_area.appendChild(privacityLabel)
            edit_area.appendChild(privacity)
            edit_area.appendChild(document.createElement("br"))
            
            edit_area.appendChild(legend)
            edit_area.appendChild(document.createElement("br"))
            edit_area.appendChild(pictures)

            edit_area.appendChild(new_pictures_wrapper) 

            edit_area.appendChild(_pics_deleted)

            edit_area.style.border = "1px solid yellow"
            edit_area.style.padding = "10px"
            edit_area.style.margin = "10px"


            posts = document.getElementById("posts")
            posts.insertAdjacentElement("afterBegin", edit_area)
        })
        .catch( error => console.log(error) )
    }
}

function edit_cancel() {
    let edit_post = document.getElementById("edit_post")
    let conf = true
    if( edit_post ){
        conf = confirm("Vc deseja cancelar esta edição?")
        if( conf ) { edit_post.remove() }
    }
    return conf
}

function edit_popImg( wImgID ) {
    let editPost = document.getElementById("edit_post")
    let wrapperImg = document.getElementById(wImgID)
    
    
    let picsDeleted = editPost.getElementsByClassName("pictures_deleted")[0] // .value = get_json_data || set_json_data
    let picsDeletedValue = null
    if( picsDeleted.value ){ picsDeletedValue = get_json_data(picsDeleted.value) }
    if( picsDeletedValue ) {
        picsDeletedValue.push(wrapperImg.getAttribute("data"))
        picsDeleted.value = set_json_data(picsDeletedValue)
    } else {
        picsDeleted.value = set_json_data(Array(wrapperImg.getAttribute("data")))
    }
    
    let btn_wrapper_img = wrapperImg.getElementsByClassName("btn_wrapper_img")[0]
    btn_wrapper_img.textContent = "Desfazer"
    btn_wrapper_img.setAttribute("onclick", `edit_unpopImg('${wImgID}')`)

    wrapperImg.style.borderColor = "#f00"
    wrapperImg.classList.remove("saved")
    wrapperImg.classList.add("deleted")

    return
}

function edit_unpopImg( wImgID ) {
    let editPost = document.getElementById("edit_post")
    let wrapperImg = document.getElementById(wImgID)

    let picsDeleted = editPost.getElementsByClassName("pictures_deleted")[0] // .value = get_json_data || set_json_data
    let picsDeletedValue = get_json_data(picsDeleted.value)

    if( picsDeletedValue ) {
        let index = picsDeletedValue.indexOf(wrapperImg.getAttribute("data"))
        picsDeletedValue.splice(index, 1)
        picsDeleted.value = set_json_data(picsDeletedValue)
    }

    let btn_wrapper_img = wrapperImg.getElementsByClassName("btn_wrapper_img")[0]
    btn_wrapper_img.textContent = "Excluir"
    btn_wrapper_img.setAttribute("onclick", `edit_popImg('${wImgID}')`)

    wrapperImg.style.borderColor = "#0f0"
    wrapperImg.classList.remove("deleted")
    wrapperImg.classList.add("saved")

    return
}

function edit_imagePreview() {
    let file = document.getElementById("edit_newImages")
    let editPost = document.getElementById("edit_post")
    let pictures = editPost.getElementsByClassName("pictures")[0]

    let pre = editPost.getElementsByClassName("pre")
    Array.from(pre).forEach(p => p.remove())

    Array.from(file.files).forEach(
        f => {
            let wrapper_img = create_wrapper_img({id:"", url: URL.createObjectURL(f)})
            wrapper_img.classList.remove("saved")
            wrapper_img.classList.add("pre")
            wrapper_img.style.border = "1px solid yellow"

            pictures.appendChild(wrapper_img)

        }
    )

    editPost.getElementsByClassName("new_picture_counter")[0].textContent = file.files.length

    return
}

function new_post_preview() {
    let imgs = document.getElementById("new_post_preview")
    let f = document.getElementById("new_post_images")
    Array.from(f.files).forEach(file => {
        let img = new Image()
        img.classList.add("img_preview")
        img.src = URL.createObjectURL(file)
        img.style.width = "100px"

        imgs.appendChild(img)
    })
    return
}