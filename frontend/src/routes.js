import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/home";
import Cadastro from "./pages/cadastro";
import Login from "./pages/login";
import Assets from "./pages/assets";
import Editar from "./pages/editar";
import MyAssets from "./pages/meusasset";

function AppRoutes() {
    return (
        <BrowserRouter>
        <Routes>
            <Route path="/" element={<Home/>}></Route>
            <Route path="/assets" element={<Assets/>}></Route>
            <Route path="/cadastro" element={<Cadastro/>}></Route>
            <Route path="/login" element={<Login/>}></Route>
            <Route path="/editar" element={<Editar/>}></Route>
            <Route path="/meuasset" element={<MyAssets/>}></Route>
        </Routes>
        </BrowserRouter>
    )
}

export default AppRoutes;