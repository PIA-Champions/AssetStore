import { Link } from "react-router-dom";
import styles from "./header.module.css";
import HeaderLink from "../HeaderLink";
import HeaderSearch from "../HeaderSearch";
import MenuDropdown from "../MenuDropdown";
import HeaderUserInfo from "../HeaderUserInfo";

function Header() {
    return (
        <header className={styles.header_container}>
            <Link to="./">
                <h1>ASSET STORE</h1>
            </Link>
            <nav>
                <HeaderLink url="./">Home</HeaderLink>
                <HeaderLink url="./assets">Assets</HeaderLink>
                <MenuDropdown />
                <HeaderSearch />
            </nav>
        </header>
    );
}
export default Header;