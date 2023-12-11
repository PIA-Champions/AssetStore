import { Link } from "react-router-dom";
import styles from "./MenuDropdown.module.css";

function MenuDropdown() {
    return (
        <div className={styles.dropdown}>
            <span className={styles.dropbtn} typeof="button" role="button">Usuário</span>
            <div className={styles.dropdown_content}>
                <Link to="./cadastro">Cadastro</Link>
                <Link to="./login">Login</Link>
                <Link to="./editar">Editar</Link>
            </div>
        </div>
    );
}

export default MenuDropdown;