import FormRegister from "../../components/FormCadastro/index.js";
import styles from "./cadastro.module.css";

function Cadastro() {
    return (
        <div className={styles.container_cadastro}>
            <h1>Cadastrar</h1> 
            <FormRegister />
        </div>
    )
}

export default Cadastro;