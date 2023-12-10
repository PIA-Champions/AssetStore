import FormRegister from "../../components/FormCadastro/index.js";
import styles from "./cadastro.module.css";

function Cadastro() {
    return (
        <div className={styles.container_cadastro}>
            <a href="./"><span class="material-icons">west</span></a>
            <h1>Cadastrar</h1> 
            <FormRegister />
        </div>
    );
}

export default Cadastro;