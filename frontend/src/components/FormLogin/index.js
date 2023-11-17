import styles from "../FormLogin/FormLogin.module.css";

function FormLogin() {
    return (
        <div className={styles.container}>
        <form>
          <label>Nome</label><br/>
          <input type="name" id="username" name="name" placeholder="Username" required/><br/>

          <label>Password</label><br/>
          <input type="password" id="password" name="password" placeholder="Password" required/><br/>

          <br/><button id='button-login' type="submit">Entrar</button>
        </form>
    </div>
    );
} 

export default FormLogin;