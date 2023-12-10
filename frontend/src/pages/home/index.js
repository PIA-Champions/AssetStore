import Header from "../../components/Header";
import styles from "./home.module.css";

function Home() {
    return (
        <div>
            <Header />
            <div className={styles.iwt_container}>
                <p>
                    Bem-vindo à Asset-Store, sua principal fonte de assets digitais para impulsionar a excelência nos seus projetos de jogos! Explore nosso extenso catálogo que abrange desde tilesets envolventes e sprites dinâmicos até modelos 3D de alta qualidade, efeitos sonoros imersivos e trilhas sonoras encantadoras. Na Asset-Store, comprometemo-nos a fornecer assets de qualidade superior a preços acessíveis, garantindo que sua jornada de desenvolvimento seja repleta de recursos excepcionais para criar experiências de jogo inesquecíveis. Descubra a diferença que os nossos assets podem fazer e eleve o nível dos seus jogos com a Asset-Store!
                </p>
                <picture></picture>
            </div>
        </div>
    );
}

export default Home;