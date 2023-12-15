// HeaderUserInfo.js
import React, { useEffect, useState } from 'react';
import { getUserInfo } from '../../UserService'; // Ajuste o caminho conforme necessário

export default function HeaderUserInfo() {
  const userId = sessionStorage.getItem("logged_user_id");
  const [userInfo, setUserInfo] = useState(null);
  
  useEffect(() => {
    if (userId) {
      async function fetchUserInfo() {
        try {
          const userInformation = await getUserInfo(userId);
          setUserInfo(userInformation);
          } catch (error) {
          console.error(error);
          }
      }

      fetchUserInfo();
    }
  }, [userId]);

  return (
            <UserInfoContent userInfo={userInfo} />
  );
}

function UserInfoContent({ userInfo }) {
  // Render user information based on userInfo
  let userName = "User not logged"
  
  if(userInfo){
    userName = userInfo.name;
  }

  return (
    <div>
      {userName}
    </div>
  );
}
