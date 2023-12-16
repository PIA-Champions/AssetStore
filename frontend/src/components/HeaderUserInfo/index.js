import styles from "../HeaderUserInfo/HeaderUserInfo.module.css";
import { jwtDecode } from "jwt-decode";

export default function HeaderUserInfo() {
  const token = sessionStorage.getItem("assetsToken");

  if (token === null) {
    var userName = 'User not logged';
  }
  else {
    const decoded = jwtDecode(token);
    var userName = decoded.sub;
  }

  return (
          <div className={styles.user_status}>
            {userName}
          </div>
  );
}