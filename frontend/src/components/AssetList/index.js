import styles from "../AssetList/AssetList.module.css";
import React, { useState, useEffect } from 'react';
import { apiUrl } from '../../ApiConfig/apiConfig.js';
import { AssetDetails } from '../AssetDetails/index.js';
import { getUserInfo } from '../../UserService'; // Ajuste o caminho conforme necessário
import { jwtDecode } from "jwt-decode";

export default function AssetList() {

  const [assets, setAssets] = useState([]);
  const [userInfo, setUserInfo] = useState([]);
  const token = sessionStorage.getItem("assetsToken");

  if (token === null) {
    var userName = 'User not logged';
  } else {

    const decodedToken = jwtDecode(token);
    var userName = decodedToken.sub;
    var userAssets = decodedToken.buyed_asset_packs;
    var userId = decodedToken.id;
  }



  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${apiUrl}/assets`, { method: 'GET' });
        const data = await response.json();
        setAssets(data["Response"]);

      } catch (error) {
        console.error('Error fetching assets:', error);
      }
    };

    fetchData();

    async function fetchUserInfo() {
      try {
        const userInformation = await getUserInfo(userId);
        setUserInfo(userInformation);
      } catch (error) {
        console.error('Error fetching logged user information:', error);
      }
    }

    if (userId) {
      fetchUserInfo();
    }
    fetchData();


  }, []); // Empty dependency array ensures that useEffect runs only once after the initial render

  let updatedAssets = assets;

  console.log(updatedAssets)

  if (userInfo && userInfo.purchased_asset_packs) {
    //Update asset with purchasing information
    updatedAssets = assets.map(asset => ({
      ...asset,
      purchased: userInfo.purchased_asset_packs.includes(asset.id),
    }));
  }

  return (
    <div className={styles.list_container}>
      <h2 className={styles.title_assets}>
        <a href="./">
          <span class="material-icons">west</span>
        </a><br />Lista de Assets
      </h2>
      <ul className={styles.assets_ul}>
        {updatedAssets.map(asset => (
          <li key={asset.id}>
            <div>
              <AssetDetails
                title={asset.title}
                id={asset.id}
                description={asset.description}
                price={asset.cost}
                download_url={asset.web_address}
                thumb_url={asset.store_media[0].web_address}
                purchased={asset.purchased}
              />
              <br />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}