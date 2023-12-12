import styles from "../AssetDetails/AssetDetails.module.css";

export function AssetDetails(param) {
    return (
        <div className={styles.card_container}>
            <h1 id="title-assets">{param.title}</h1>
            <figure className={styles.image_container}>
                <img className={styles.image_card} src={param.thumb_url}/>
            </figure>
            <h3 id="description-assets">{param.description}</h3>
            <h2 id="price-assets">{param.price} coins</h2>
            <button className="btn_assets">Comprar</button>
        </div>
    );
}
