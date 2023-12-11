import Header from "../../components/Header";
import styles from "./home.module.css";

function Home() {
    return (
        <div className={styles.container_header}>
            <Header />
            <div className={styles.iwt_container}>
                <p>
                    <p>Bem-vindo à Asset-Store, a sua principal fonte de assets digitais.</p>
                    <p>Explore nosso extenso catálogo, que abrange desde tilesets envolventes, e sprites dinâmicos, até modelos 3D de alta qualidade, efeitos sonoros imersivos e trilhas sonoras encantadoras.</p>
                    <p>Na Asset-Store, comprometemo-nos a fornecer qualidade superior com preços acessíveis, garantindo que sua jornada de desenvolvimento seja repleta de recursos excepcionais.</p>
                    <p>Descubra a diferença que os nossos assets podem fazer, e eleve o nível dos seus jogos para criar experiências inesquecíveis.</p>
                </p>
                <picture></picture>
            </div>
            <h5 className={styles.copyright}>
                © 2023 - All Rights Reserved - Assetstore
            </h5>
        </div>
    );
}

export default Home;