import FormLogin from "../../components/FormLogin/index.js";
import styles from "../login/login.module.css";

function Login() {
    return (
        <div className={styles.container_login}>
            <a href="./cadastro"><span class="material-icons">west</span></a>
            <h1>Área do usuário</h1>
            <FormLogin />
        </div>
    );
}

export default Login;