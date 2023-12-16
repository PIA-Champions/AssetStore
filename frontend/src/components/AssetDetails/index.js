import styles from "../AssetDetails/AssetDetails.module.css";

export function AssetDetails(param) {
    const buttonText = "Comprar";
    if(param.purchased){
        buttonText = "Download"
    }
    return (
        <div className={styles.card_container}>
            <h1 id="title-assets">{param.title}</h1>
            <figure className={styles.image_container} loading="lazy">
                <img className={styles.image_card} src={param.thumb_url} loading="lazy"/>
            </figure>
            <h3 id="description-assets">{param.description}</h3>
            <h2 id="price-assets">{param.price} coins</h2>
            <button className={styles.btn_assets}>{buttonText}</button>
        </div>
    );
}
