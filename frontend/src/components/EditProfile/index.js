import styles from '../EditProfile/EditProfile.module.css';

function EditProfile() {
    return (
        <div className={styles.container_edit}>
            <a href="./"><span class="material-icons">west</span></a>
            <h1>Alterar dados</h1>
            <div className={styles.container}>
                <form className={styles.container_form}>
                    <label>E-mail</label><br />
                    <input type="name" id="emailEdit" name="name" placeholder="Email"/><br/>

                    <label>Password</label><br />
                    <input type="password" id="passwordEdit" name="password" placeholder="Password"/><br/>

                    <label>Balance</label><br />
                    <input className={styles.input_balance} type="number" id="balanceEdit" name="balance" placeholder="Balance"/><br/>
                    <a type="button" className={styles.balance_button}>✔</a>

                    <br/><button className={styles.button_ok} type="submit">confirmar alterações</button>
                </form>
            </div>
        </div>
    );
}

export default EditProfile;