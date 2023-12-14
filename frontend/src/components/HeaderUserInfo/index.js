import React, { useEffect } from 'react';
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
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${apiUrl}/user/${userId}`, { method: 'GET' });
                const data = await response.json();
                console.log(data);
                return data;
            } catch (error) {
                console.error('Error fetching logged user data:', error);
            }
        };

            return fetchData();

    }); 
}
