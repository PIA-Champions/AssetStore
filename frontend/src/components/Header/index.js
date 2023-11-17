import { Link } from "react-router-dom";
import styles from "./header.module.css";
import HeaderLink from "../HeaderLink";
import HeaderSearch from "../HeaderSearch";

function Header() {
    return (
        <header className={styles.header}>
            <Link to="./">
                <h1>
                    ASSET STORE
                </h1>
            </Link>
            <nav>
                <HeaderLink url="./">Home</HeaderLink>
                <HeaderLink url="./assets">Assets</HeaderLink>
                <HeaderLink url="./cadastro">Cadastro</HeaderLink>
                <HeaderLink url="./login">Login</HeaderLink>
                <HeaderSearch />
            </nav>
        </header>
    );
}

export default Header;