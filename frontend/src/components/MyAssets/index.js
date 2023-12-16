import styles from "../MyAssets/MyAssets.module.css";

function MyAssets() {
    return (
        <div className={styles.my_header}>
            <a href="./"><span class="material-icons">west</span></a>
            <h1 className={styles.my_header_title}>Meus Assets</h1> 
            <div className={styles.my_card_container}>
                <h1 id="my-title-assets">Teste</h1>
                <figure className={styles.my_image_container} loading="lazy">
                    <img className={styles.my_image_card} loading="lazy"/>
                </figure>
                <h3 id="my-description-assets">Teste</h3>
                <button className={styles.my_btn_assets}>Download</button>
            </div>
        </div>
    );
}

export default MyAssets;