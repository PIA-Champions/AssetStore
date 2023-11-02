import { Link } from "react-router-dom";
import styles from "./header.module.css";
import HeaderLink from "../HeaderLink";
import HeaderSearch from "../HeaderSearch";

function Header() {
    return (
        <header className={styles.header}>
            <Link to="./">
                <h1>
                    Asset Store
                </h1>
            </Link>
            <nav>
                <HeaderLink url="./">Home</HeaderLink>
                <HeaderLink url="./about">About</HeaderLink>
                <HeaderLink url="./assets">Kit Assets</HeaderLink>
            </nav>
            <HeaderSearch />
        </header>

    )
}

export default Header;