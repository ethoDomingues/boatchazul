
function create_peview_group_element( group ) {
    let div_group_recomm = document.createElement("div")
    div_group_recomm.classList.add("recommended")
    div_group_recomm.setAttribute("id", group.id)

    let name_group_recomm = document.createElement("a")
    name_group_recomm.setAttribute("href", URL_webui_group + group.id)
    name_group_recomm.textContent = group.name

    let counter_group_recomm = document.createElement("div")
    counter_group_recomm.textContent = group.members.ids.length + " Membros"
    counter_group_recomm.classList.add(`counter_group_handler_${group.id}`)

    let group_entry = document.createElement("div")

    if( group.entry ){
        group_entry.textContent = "Fechado"
    } else {
        group_entry.textContent = "Aberto"
    }


    let btn_group_recomm = create_btn_group( group )

    div_group_recomm.appendChild(name_group_recomm)
    div_group_recomm.appendChild(group_entry)
    div_group_recomm.appendChild(btn_group_recomm)
    div_group_recomm.appendChild(counter_group_recomm)
    
    return div_group_recomm
}

function create_new_group_form() {
    form = document.getElementById("new_group_form")

    btn_new_group = document.getElementById("btn_new_group")
    btn_new_group.setAttribute("onclick", "remove_new_group_form()")
    btn_new_group.textContent = "Cancelar"

    group_name = document.createElement("input")
    group_name.type = "text"
    group_name.setAttribute("name", "name")
    group_name.setAttribute("id", "new_group_name")
    group_name.setAttribute("placeholder", "Nome do Grupo")

    div_name = document.createElement("div")
    div_name.appendChild(group_name)

    
    group_entry = document.createElement("input")
    group_entry.type = "checkbox"
    group_entry.setAttribute("name", "entry")
    group_entry.setAttribute("id", "new_group_entry")

    group_entry_label = document.createElement("label")
    group_entry_label.textContent = "Grupo Fechado ( usuários solicitarão a entrada )"
    group_entry_label.setAttribute("for", "new_group_entry")

    div_entry = document.createElement("div")
    div_entry.appendChild(group_entry)
    div_entry.appendChild(group_entry_label)

    

    group_desc = document.createElement("textarea")
    group_desc.setAttribute("name", "description")
    group_desc.setAttribute("id", "new_group_description")
    group_desc.setAttribute("placeholder", "Descrição do Grupo")

    div_desc = document.createElement("div")
    div_desc.appendChild(group_desc)

    btnSave = document.createElement("button")
    btnSave.textContent = "Criar"
    btnSave.setAttribute("onclick", "save_group()")

    form.appendChild(div_name)
    form.appendChild(div_entry)
    form.appendChild(div_desc)
    form.appendChild(btnSave)


}

function remove_new_group_form() {
    recomm = document.getElementById("new_group_form")

    btn_new_group = document.getElementById("btn_new_group").cloneNode()
    btn_new_group.setAttribute("onclick", "create_new_group_form()")
    btn_new_group.textContent = "Criar Grupo"
    
    form = document.createElement("div")
    form.setAttribute("id", "new_group_form")
    
    recomm.innerHTML = ""
    
    recoom.appendChild(btnSave)
    recomm.appendChild(form)
}

function create_btn_group( group ){
    let btn_group = document.createElement("button")
    
    let imOwner = group.owners.ids.includes(currentUser.id)
    let imMember = group.members.ids.includes(currentUser.id)
    let iAskedToEnter = group.solicitations.ids.includes(currentUser.id)
    
    btn_group.classList.add(`btn_group_handler_${group.id}`)


    if( imOwner) {

        btn_group.textContent = "Excluir Grupo"
        btn_group.setAttribute("onclick", `del_group('${group.id}')` )

    } else if( imMember ) {

        btn_group.textContent = "Sair"
        btn_group.setAttribute("onclick", `exit_group('${group.id}')` )

    } else if( iAskedToEnter ){

        btn_group.textContent = "Cancelar solicitação"
        btn_group.setAttribute("onclick", `exit_group('${group.id}')` )

    } else {

        btn_group.setAttribute("onclick", `enter_group('${group.id}')` )
        if( ! group.entry ){ btn_group.textContent = "Entrar" }
        else { btn_group.textContent = "Solicitar Entrada" }
        
    }

    return btn_group
}


