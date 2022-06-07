function load() {
    document.getElementById("btn_new_group").setAttribute("onclick", "create_new_group_form()")
    
    let h = new Headers({Authorization: JWT})

    loadUserData.then(
        fetch(URL_group_get_all,{headers: h})
        .then( response => response.json())
        .then( data => {
            let recomm = document.getElementById("recommended_wrapper")
            let my_groups = document.getElementById("my_groups_wrapper")
            data.groups.forEach(group => {
                if( group.members.ids.includes(currentUser.id) ){
                    my_groups.appendChild( create_peview_group_element( group ) )
                } else {
                    recomm.appendChild( create_peview_group_element( group ) )
                }
            })
        })
        .catch( error => { console.log(error) })
    )
}

function save_group() {
    let group_name = document.getElementById("new_group_name")
    let group_desc = document.getElementById("new_group_description")
    let group_entry = document.getElementById("new_group_entry")

    if( group_name.value  ) {
        let h = new Headers()
        h.append("Authorization", JWT)
        h.append('Accept', 'application/json')
        h.append('Content-Type', 'application/json')
    
        fetch( URL_group_post,{
            headers: h,
            method: "post",
            body: JSON.stringify({
                name: group_name.value,
                entry: group_entry.checked,
                description: group_desc.value
            })
        })
        .then( response => response.json() )
        .then( data => { 
            let recomm = document.getElementById("recommended_wrapper")
            recomm.insertAdjacentElement("afterBegin", create_peview_group_element( data ) )

            group_name.value = ""
            group_desc.value = ""
            group_entry.checked = false
        })
        .catch( error => { console.log( error )})
    }
}

function enter_group( groupID ){
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch(URL_grouphook + groupID, {
        headers: h,
        method: "post",
        body: JSON.stringify({user: currentUser.id})
    })
    .then( response => response.json() )
    .then( data =>  update_btn_group_handler( data ) )
    .catch( error => { console.log( error ) })
    return
}

function exit_group( group ){
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch(URL_grouphook + group,{
        headers: h,
        method: "delete",
        body: JSON.stringify({user: currentUser.id})
    })
    .then( response => response.json() )
    .then( data => update_btn_group_handler( data ) )
    .catch( error => { console.log( error ) })
    return
}

function del_group( data ){
    let h = new Headers()
    h.append("Authorization", JWT)
    h.append('Accept', 'application/json')
    h.append('Content-Type', 'application/json')

    fetch( URL_group + group,{
        headers: h,
        method: "delete",
    })
    .then( response => { 
        if(200 < response.status < 300 ) { document.getElementById(group).remove() }
    })
    .catch( error => { console.log( error ) })
    return
}


function update_btn_group_handler( data ){

    let btn = document.getElementsByClassName(`btn_group_handler_${data.id}`)[0]
    btn.insertAdjacentElement("beforeBegin", create_btn_group( data ))
    btn.remove()

    let counter = document.getElementsByClassName(`counter_group_handler_${data.id}`)[0]
    counter.textContent = data.members.ids.length + " Membros"
    return
}
