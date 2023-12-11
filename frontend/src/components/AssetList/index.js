import React, { useState, useEffect } from 'react';
import { apiUrl } from '../../ApiConfig/apiConfig.js';
//import { AssetDetails } from '../AssetDetails/index.js';

export default function AssetList() {
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${apiUrl}/assets`, { method: 'GET' });
        const data = await response.json();
        console.log(data);
        setAssets(data);
      } catch (error) {
        console.error('Error fetching assets:', error);
      }
    };

    fetchData();
  }, []); // Empty dependency array ensures that useEffect runs only once after the initial render

  return (
    <div>
      <h2>Lista de Assets</h2>
      <ul>
        " todo "
      </ul>
    </div>
  );
}
