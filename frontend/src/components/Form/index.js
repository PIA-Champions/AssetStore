import styles from '../Form/form.module.css';

function FormRegister() {
  return (
    <div className={styles.container}>
      <div id="form-login">
        <form>
          <label>Nome</label>
          <input type="name" id="inputName" name="name" />

          <label>E-mail</label>
          <input type="email" id="inputEmail" name="email" />

          <label>Password</label>
          <input type="password" id="inputPassword" name="password" />

          <button type="submit">Concluir</button>
        </form>
      </div>
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