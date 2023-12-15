// HeaderUserInfo.js
import React, { useEffect, useState } from 'react';
import { getUserInfo } from '../../UserService'; // Ajuste o caminho conforme necessário
import styles from "../MenuDropdown/MenuDropdown.module.css";

export default function HeaderUserInfo() {
  const userId = sessionStorage.getItem("logged_user_id");
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      async function fetchUserInfo() {
        try {
          const userInformation = await getUserInfo(userId);
          setUserInfo(userInformation);
        } finally {
          setLoading(false);
        }
      }

      fetchUserInfo();
    }
  }, [userId]);

  return (
            <UserInfoContent userInfo={userInfo} userId = {userId} />
  );
}

function UserInfoContent(param) {
  // Render user information based on userInfo
  let userName = "User not logged"; 
  let userBalance = "";
  let userId = "";
  
  if(param.userInfo){
    userName = param.userInfo.name;
    userBalance = param.userInfo.balance;
    userId = param.userId;
  }

  return (
    
    <div className={styles.dropdown}>
    <span className={styles.dropbtn} typeof="button" role="button">{userName}</span>
    <div className={styles.dropdown_content}>
        <p>Saldo: {userBalance} Coins</p>
        <p>{userId} </p>
    </div>
    </div>

  );
}

