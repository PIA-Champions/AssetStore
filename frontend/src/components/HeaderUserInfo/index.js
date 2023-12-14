import { apiUrl } from '../../ApiConfig/apiConfig.js';

export default function HeaderUserInfo() {
    var userId = null;
    userId = sessionStorage.getItem("logged_user_id");    
    if(!userId){
        return (
            <div>
                User not logged
            </div>
        );
    }

    const loggedUserInfo = GetUserInfo(userId);
    
    return (
        <div>
            User Name
        </div>
    );
}


function GetUserInfo(userId){
    try{
        fetch(`${apiUrl}/user/${userId}`,{
            method: 'GET',
            mode: "cors",
        })
        .then(response=>response.json())
        .then(data=>{
            console.log(data);
            return data;
        })
    }catch (error) {
        console.error(error);
    }
    
}
