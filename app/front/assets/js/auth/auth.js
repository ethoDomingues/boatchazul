const currentUser = Object()


function setAccessToken( jwt ) { window.localStorage.setItem( "accessToken", jwt ) }
function remAccessToken() { window.localStorage.removeItem( "accessToken" ) }
function getAccessToken() { return window.localStorage.getItem( "accessToken" ) }

function loadUserID(){
    let [ ,token] = JWT.split(" ")
    let [ ,payload, ] = token.split(".")
    currentUser.id = JSON.parse(decodeURIComponent(atob(payload))).userID
    return
}
function remUserID(){ window.localStorage.removeItem("userID") }
function setUserID( jwt ){
    if( jwt.includes("Bearer ") ){
        jwt = jwt.substring(7)
        let jwt_split = jwt.split(".")
        if( jwt_split.length != 3 ){ return null }
        let payload = JSON.parse(decodeURIComponent(jwt_split[1]))
        window.localStorage.setItem( "userID", payload.userID )
        return payload.userID
    } else { return null }
}

function loggout() {
    axios.delete(URL_login)
    .then( response => {
        remAccessToken()
        remUserID()
        window.location.href = URL_login
    })
    .catch((error) => { console.log(error) })
}

const loadUserData = new Promise(
    function(resolve, reject) {
        loadUserID()
        if( currentUser.id ){
            let h = new Headers({Authorization: JWT})
            fetch( URL_users + currentUser.id, {headers:h})
            .then( response => response.json() )
            .then( data => {
                Object.keys(data).forEach( attr => { currentUser[attr] = data[attr] })
                resolve()
            } )
            .catch( error => { reject( error ) } )
        }
    }
)

