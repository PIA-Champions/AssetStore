import { Link } from "react-router-dom";
import styles from "./MenuDropdown.module.css";

function MenuDropdown() {
    return (
        <div className={styles.dropdown}>
            <span className={styles.dropbtn} typeof="button" role="button">Área do usuário</span>
            <div className={styles.dropdown_content}>
                <Link to="./cadastro">Cadastro</Link>
                <Link to="./login">Login</Link>
                <Link to="./editar">Editar dados</Link>
            </div>
        </div>
    );
}

export default MenuDropdown;