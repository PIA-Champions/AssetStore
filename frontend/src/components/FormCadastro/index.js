import styles from '../FormCadastro/form.module.css';
import { useState } from 'react';
import { apiUrl } from '../../ApiConfig/apiConfig.js';

export default function FormRegister() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(false);

  const handleName = (event) => {
    setName(event.target.value);
    setSubmitted(false);
  }

  const handleEmail = (event) => {
    setEmail(event.target.value);
    setSubmitted(false);
  }

  const handlePassword = (event) => {
    setPassword(event.target.value);
    setSubmitted(false);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    if (name === '' || email === '' || password === '') {
      setError(true);
    } else {
      try {
        
        fetch('${apiUrl}/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          mode: "cors",
          body: JSON.stringify({
            name: name,
            //email: email,
            password: password
          })
        })
          .then(response => response.json())
          .then(data => {
            if (data.Response === "ITEM_ALREADY_EXISTS") {
              setError(true);
            }
            else {
              setSubmitted(true);
              setError(false);
            }
          })
          .catch(error => {
            console.error(error);
          });

      } catch (error) {
        setError(true);
        console.log(error);
      }

      //setSubmitted(true);
      //setError(false);
    }
  }

  const successMessage = () => {
    return (
      <div className={styles.success}>
        <h3>Conta criada com sucesso!</h3>
      </div>
    );
  }

  const errorMessage = () => {
    return (
      <div className={styles.error}>
        <h3>Por favor, preencha todos os campos.</h3>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit}>
        <label>Nome</label><br />
        <input type="name" id="inputName" name="name" placeholder="Username" value={name} onChange={handleName} required /><br />

        <label>E-mail</label><br />
        <input type="email" id="inputEmail" name="email" placeholder="Email" value={email} onChange={handleEmail} required /><br />

        <label>Password</label><br />
        <input type="password" id="inputPassword" name="password" placeholder="Password" value={password} onChange={handlePassword} required /><br />

        <br /><button id='button-form' type="submit">Concluir</button>
      </form>
      <h3> Já tem uma conta? <a href="http://localhost:3000/login">Clique aqui.</a></h3>
      {submitted && successMessage()}
      {error && errorMessage()}
    </div>
  );
}