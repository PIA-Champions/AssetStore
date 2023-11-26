import styles from "../FormLogin/FormLogin.module.css";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function FormLogin() {
    const [name, setName] = useState(''); // [variável, função que atualiza a variável]
    const [password, setPassword] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [error, setError] = useState(false);
    const navigate = useNavigate();

    const successMessage = () => {
        return (
            <div className={styles.success}>
                <p>Usuário logado com sucesso!</p>
            </div>
        );
    }

    const errorMessage = () => {
        return (
            <div className={styles.error}>
                <p>Usuário ou senha inválidos!</p>
            </div>
        );
    }

    const handleName = (event) => {
        setName(event.target.value);
        setSubmitted(false);
    }

    const handlePassword = (event) => {
        setPassword(event.target.value);
        setSubmitted(false);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        if (name === '' || password === '') {
            setError(true);
        }
        else {
            try {
                fetch('https://ckf9b5do98.execute-api.us-east-1.amazonaws.com/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        // 'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    mode: "cors",
                    body: JSON.stringify({
                        name: name,
                        password: password
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.Response)
                        if (data.Response === "INVALID_INPUT_DATA") {
                            setError(true);
                        }
                        else {
                            const token = data.Token;
                            sessionStorage.setItem("assetsToken", token);
                            setSubmitted(true);
                            setError(false);
                            navigate('/');
                        }
                    })
                    .catch(error => {
                        console.error(error);
                    });
            } catch (error) {
                console.error(error);
            }
        }
    }

    return (
        <div className={styles.container}>
            <form onSubmit={handleSubmit}>
                <label>Nome</label><br />
                <input type="name" id="username" name="name" placeholder="Username" value={name} onChange={handleName} required /><br />

                <label>Password</label><br />
                <input type="password" id="password" name="password" placeholder="Password" value={password} onChange={handlePassword} required /><br />

                <br /><button id='button-login' type="submit">Entrar</button>
            </form>
            {submitted && successMessage()}
            {error && errorMessage()}
        </div>
    );
}

export default FormLogin;