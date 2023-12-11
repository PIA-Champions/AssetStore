//Component for listing all assets
import React, { useState, useEffect } from 'react';

const AssetList = () => {
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    // Method for fetching assets from backend
    const fetchAssets = async () => {
      try {
        const response = await fetch('${apiUrl}/assets');
        const data = await response.json();
        setAssets(data.Response);
      } catch (error) {
        console.error('Error fetching assets:', error);
      }
    };

    // Call the method for fetching assets when the component is mounted
    fetchAssets();
  }, []); // The empty array assures the code will be called one time only

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
