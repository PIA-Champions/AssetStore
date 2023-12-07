import styles from '../editar/editar.module.css'

function Editar() {
    return (
        <div className={styles.container_edit}>
            <a href="./"><span class="material-icons">west</span></a>
            <h1>Alterar dados</h1>
            <div className={styles.container}>
                <form>
                    <label>E-mail</label><br />
                    <input type="name" id="emailEdit" name="name" placeholder="Email"/><br/>

                    <label>Password</label><br />
                    <input type="password" id="passwordEdit" name="password" placeholder="Password"/><br/>

                    <label>Balance</label><br />
                    <input type="number" id="balanceEdit" name="password" placeholder="Balance"/><br/>
                    <a type="button" className="balanceButton">✔</a>

                    <br /><button id="buttonOk" type="submit">Pronto</button>
                </form>
            </div>
        </div>
    );
}

export default Editar;