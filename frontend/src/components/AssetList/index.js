import React, { useState, useEffect } from 'react';
import { apiUrl } from '../../ApiConfig/apiConfig.js';
import { AssetDetails } from '../AssetDetails/index.js';
import { getUserInfo } from '../../UserService'; // Ajuste o caminho conforme necessário

export default function AssetList() {
  
  const [assets, setAssets] = useState([]);
  const [userInfo, setUserInfo] = useState([]);
  const userId = sessionStorage.getItem("logged_user_id");
  
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

    async function fetchUserInfo() {
      try {
        const userInformation = await getUserInfo(userId);
        setUserInfo(userInformation);
      } catch (error) {
        console.error('Error fetching logged user information:', error);
      }
    }

    if(userId){
      fetchUserInfo();
    }
    fetchData();
     
  }, []); // Empty dependency array ensures that useEffect runs only once after the initial render

  let updatedAssets = assets;
  if(userInfo && userInfo.purchased_asset_packs){
      //Update asset with purchasing information
      updatedAssets = assets.map(asset => ({
        ...asset,
        purchased: userInfo.purchased_asset_packs.includes(asset.id),
      }));
  } 
  
  return (
    <div>
      <h2>Lista de Assets</h2>
      <ul>
      {updatedAssets.map(asset => (
          <li key={asset.id}>   
            <div>
              <AssetDetails 
                title={asset.title} 
                description={asset.description}
                price={asset.cost}
                thumb_url={asset.store_media[0].web_address}
                purchased = {asset.purchased}
              />
              <br/>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
