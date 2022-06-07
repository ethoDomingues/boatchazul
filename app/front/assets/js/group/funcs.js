



const loadGroupData = new Promise(function( resolve, reject ){
    let h = new Headers({Authorization: JWT})
    fetch( URL_group + currentGroup.id, { headers: h } )
    .then( response => response.json() )
    .then( data => {
        Object.keys(data).forEach( k => { currentGroup[k] = data[k] })
        resolve()
    })
    .catch( error => { reject( error ) } )
})


function loadGroup() {
    loadUserData.then( function() {
        loadGroupData.then( function(){
            
            create_new_post_form()
            
            let userIsMod = currentGroup.mods.ids.includes(currentUser.id)
            let userIsAdmin = currentGroup.admins.ids.includes(currentUser.id)
            let userIsOwner = currentGroup.owners.ids.includes(currentUser.id)

            if( currentGroup.entry && ( userIsMod | userIsAdmin | userIsOwner) ){
                create_user_solicitations_element()
            } else {
                document.getElementById("solicitations").remove()
            }

            currentGroup.posts.forEach(p => { setPostUI(p) })

        })
    })
}


function accept_user( user ){
    let h = new Headers({Authorization: JWT})
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch(URL_grouphook + currentGroup.id, {
        headers: h,
        method: "put",
        body: JSON.stringify({user: user})
    })
    .then( response => { console.log(response) })
    .catch( error => { console.log(error) })
}

