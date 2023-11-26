import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/home";
import Cadastro from "./pages/cadastro";
import Login from "./pages/login";

function AppRoutes() {
    return (
        <BrowserRouter>
        <Routes>
            <Route path="/" element={<Home/>}></Route>
            <Route path="/cadastro" element={<Cadastro/>}></Route>
            <Route path="/login" element={<Login/>}></Route>
        </Routes>
        </BrowserRouter>
    )
}

export default AppRoutes;