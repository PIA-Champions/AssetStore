import styles from './form.module.css';

function FormRegister() {
  return (
    <div className={styles.container}>
        <form>
          <label>Nome</label><br/>
          <input type="name" id="inputName" name="name" placeholder="Username" required/><br/>

          <label>E-mail</label><br/>
          <input type="email" id="inputEmail" name="email" placeholder="Email" required/><br/>

          <label>Password</label><br/>
          <input type="password" id="inputPassword" name="password" placeholder="Password" required/><br/>

          <br/><button id='button-form' type="submit">Concluir</button>
        </form>
        <h3> Já tem uma conta? <a href="./login">Clique aqui.</a></h3>
    </div>
  )
}

export default FormRegister;



















// https://www.webdevdrops.com/react-forms-validacao-react-hook-form/
// export default FormRegister;

// import React from "react";
// import { useForm } from "react-hook-form";
// import "./LoginForm.css";

// const LoginForm = () => {
//   const { register, handleSubmit, errors } = useForm();

//   function onSubmit(data) {
//     console.log("Data submitted: ", data);
//   }

//   return (
//     <div className="login-form">
//       <form onSubmit={handleSubmit(onSubmit)} noValidate>
//         <label htmlFor="inputEmail">E-mail</label>
//         <input
//           type="email"
//           id="inputEmail"
//           name="email"
//           ref={register({
//             required: "Enter your e-mail",
//             pattern: {
//               value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
//               message: "Enter a valid e-mail address",
//             },
//           })}
//         />
//         {errors.email && <p className="error">{errors.email.message}</p>}

//         <label htmlFor="inputPassword">Password</label>
//         <input
//           type="password"
//           id="inputPassword"
//           name="password"
//           ref={register({ required: "Enter your password" })}
//         />
//         {errors.password && <p className="error">{errors.password.message}</p>}

//         <button type="submit">Login</button>
//       </form>
//     </div>
//   );
// };

// export default LoginForm;