// AssetList.js

import React, { useState, useEffect } from 'react';

const AssetList = () => {
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    // Função para buscar assets do backend
    const fetchAssets = async () => {
      try {
        const response = await fetch('URL_DO_SEU_BACKEND/assets');
        const data = await response.json();
        setAssets(data.Response);
      } catch (error) {
        console.error('Erro ao buscar assets:', error);
      }
    };

    // Chama a função para buscar os assets quando o componente é montado
    fetchAssets();
  }, []); // O array vazio assegura que o useEffect será executado apenas uma vez

  return (
    <div>
      <h2>Lista de Assets</h2>
      <ul>
        {assets.map((asset) => (
          <li key={asset.id}>
            <strong>{asset.title}</strong> - {asset.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AssetList;
