import styles from "../AssetDetails/AssetDetails.module.css";
import { apiUrl } from '../../ApiConfig/apiConfig.js';
import fileDownload from 'js-file-download'

export function AssetDetails(param) {
    var buttonText = "Comprar";
    if(param.purchased){
        buttonText = "Download"
    }

    const token = sessionStorage.getItem("assetsToken");

    const handleBottonAction = () => {
        if(param.purchased){
            fetch(`${param.download_url}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/zip'
                }
            }).then(response => response.blob(),
            ).then(blob =>
                {  fileDownload(blob, 'filename.zip')})

            

            console.log(param.download_url)
            alert("Download");
        }else{
            fetch(`${apiUrl}/asset/${param.id}/purchase`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': `${token}`
                },
                mode: "cors",
                body: JSON.stringify({
                    user_id: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data["Message"] === "Not enough balance for purchase") {
                    alert('Saldo insuficiente!');
                }
                else if (data["Message"] === "Item already purchased") {
                    alert('Item já comprado!');
                }
                else {
                    alert('Compra realizada com sucesso!');
                }

                console.log(data);
                
            })
            .catch(error => {
                console.log(error);
                alert('Erro ao realizar compra!');
            });
        }
    }

    return (
        <div className={styles.card_container}>
            <h1 id="title-assets">{param.title}</h1>
            <figure className={styles.image_container} loading="lazy">
                <img className={styles.image_card} src={param.thumb_url} loading="lazy"/>
            </figure>
            <h3 id="description-assets">{param.description}</h3>
            <h2 id="price-assets">{param.price} coins</h2>
            <button onClick={handleBottonAction} className={styles.btn_assets}>{buttonText}</button>
        </div>
    );
}
