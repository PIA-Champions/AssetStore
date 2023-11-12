import FormRegister from "../../components/Form/index.js";
import styles from "./cadastro.module.css";
// import Header from "../../components/Header";


function Cadastro() {
    return (
        <div className={styles.container_form}>
            {/* <Header /> */} 
            <h1>Cadastrar</h1> 
            <FormRegister />
        </div>
    )
}

export default Cadastro;