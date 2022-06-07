



function create_userarea_solicitation_element( user ) {

    let img_profile = new Image()
    let userArea = document.createElement("div")
    let username = document.createElement("p")
    
    img_profile.classList.add("user_profile")
    
    if(user.profile){ img_profile.src = user.profile.img.url }
    else { img_profile.src = "/assets/img/batata.jpg" }

    img_profile.classList.add(`user_profile_${user.id}`)
    img_profile.style.width = "30px"

    userArea.classList.add("user_area")
    userArea.appendChild(img_profile)

    username.textContent = " @" + user.username

    userArea.appendChild(username)


    return userArea
}


function create_user_solicitations_element(){
    let solicitations = document.getElementById("solicitations")
    let solicitations_title = document.createElement("h3")
    let solicitations_title_counter = document.createElement("span")
    let solicitations_wrapper = document.createElement("div")

    solicitations.appendChild(solicitations_title)
    solicitations.appendChild(solicitations_wrapper)

    solicitations_title.appendChild(solicitations_title_counter)
    solicitations_title.classList.add("solicitations_title")
    solicitations_title.textContent = "Solicitações - " + currentGroup.solicitations.ids.length

    solicitations_title_counter.classList.add("solicitations_title_counter")
    solicitations_title_counter.textContent = currentGroup.solicitations.length

    solicitations_wrapper.classList.add("solicitations_wrapper")
    currentGroup.solicitations.users.forEach( user => {
        let sol = document.createElement("div")
        sol.classList.add("solicitations")
        sol.setAttribute("id",`solicitations_${user.id}`)

        sol.appendChild(create_userarea_solicitation_element(user))

        let btn_accept = document.createElement("button")
        btn_accept.setAttribute("onclick", `accept_user( '${user.id}' )`)
        btn_accept.classList.add(`btn_accept_user_${user.id}`)
        btn_accept.textContent = "Aceitar"

        sol.appendChild(btn_accept)

        solicitations_wrapper.appendChild(sol)
    })
}