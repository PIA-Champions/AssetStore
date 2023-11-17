import FormLogin from "../../components/FormLogin/index.js";
import styles from "../login/login.module.css";

function Login() {
    return (
        <div className={styles.container_login}>
            <a href="/">Voltar</a>
            <h1>Área do usuário</h1>
            <FormLogin />
        </div>
    );
}

export default Login;