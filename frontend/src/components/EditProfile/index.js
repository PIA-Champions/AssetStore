import styles from '../EditProfile/EditProfile.module.css';
import { useState } from 'react';
import { apiUrl } from '../../ApiConfig/apiConfig.js';
import { jwtDecode } from "jwt-decode";

function EditProfile() {

    const [balance, setBalance] = useState('');

    const handleBalance = (event) => {
        event.preventDefault();
        if (balance === '' || balance <= 0) {
            alert('Insira um valor positivo!');
        }
        else {

            const token = sessionStorage.getItem("assetsToken");
            const decodedToken = jwtDecode(token);
            const user_id = decodedToken.sub;

            fetch(`${apiUrl}/user/${user_id}/buy-credits`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': `${token}`,
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                mode: "cors",
                body: JSON.stringify({
                    balance: balance
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    alert('Saldo alterado com sucesso!');
                })
                .catch(error => {
                    console.log(error);
                    alert('Erro ao alterar saldo!');
                })
        }
    }

    const handleBalanceValue = (event) => {
        setBalance(event.target.value);
    }


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
                    <input className={styles.input_balance} type="number" id="balanceEdit" name="balance" placeholder="Balance" onChange={handleBalanceValue}/><br/>
                    <a href='botaodesaldo' onClick={handleBalance} type="button" className={styles.balance_button}>✔</a>

                    <br/><button className={styles.button_ok} type="submit">confirmar alterações</button>
                </form>
            </div>
        </div>
    );
}

export default EditProfile;