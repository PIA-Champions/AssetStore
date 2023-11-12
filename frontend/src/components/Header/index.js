import { Link } from "react-router-dom";
import styles from "./header.module.css";
import HeaderLink from "../HeaderLink";
import HeaderSearch from "../HeaderSearch";

const dimension = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

function Header() {
    if (dimension > 1280) {
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
                    <HeaderSearch />
                </nav>
            </header>
        )
    } else {
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
                </nav>
            </header>
        )
    }
}

export default Header;