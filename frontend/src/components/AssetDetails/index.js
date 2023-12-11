import styles from "../AssetDetails/AssetDetails.module.css";

export default function AssetDetails() {
    return (
        <div className={styles.card_container}>
            <h1 id="title-assets">RPG Asset</h1>
            <figure className={styles.image_card}/>
            <h3 id="description-assets">Descrição do produto aqui! Descrição do produto aqui! Descrição do produto aqui! Descrição do produto aqui!</h3>
            <h2 id="price-assets">R$50,00</h2>
            <button className="btn_assets">Comprar</button>
        </div>
    );
}
