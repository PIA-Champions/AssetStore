//Component for listing all assets
import { apiUrl } from '../../ApiConfig/apiConfig.js';

// Method for fetching assets from backend
export default function  AssetList(){
    try {
        fetch('${apiUrl}/assets',{method:'GET'})
        .then (response => response.json())
        .then (data => console.log(data));

        return (
          <div>
            <h2>Lista de Assets</h2>
            <ul>
                
            </ul>
          </div>
        );
    } catch (error) {
      console.error('Error fetching assets:', error);
    }
};
