import { Link } from "react-router-dom";
import styles from "./MenuDropdown.module.css";

function MenuDropdown() {

    const logout = () => {
        sessionStorage.removeItem("logged_user_id");
        sessionStorage.removeItem("assetsToken");
        window.location.reload();
    }

    const userId = sessionStorage.getItem("logged_user_id");
    
    if (userId) {
        return (
            <div className={styles.dropdown}>
                <span className={styles.dropbtn} typeof="button" role="button">Usuário</span>
                <div className={styles.dropdown_content}>
                    <Link to="./editar">Editar</Link>
                    <button onClickCapture={logout}>
                            logout
                        </button>
                </div>
            </div>
        );
    }

    else {
        return (
            <div className={styles.dropdown}>
                <span className={styles.dropbtn} typeof="button" role="button">Usuário</span>
                <div className={styles.dropdown_content}>
                    <Link to="./cadastro">Cadastro</Link>
                    <Link to="./login">Login</Link>
                </div>
            </div>
        );
    }
}

export default MenuDropdown;