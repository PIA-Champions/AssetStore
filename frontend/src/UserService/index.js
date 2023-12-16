
/*
    This module encapsulates fetching user information 
*/
import { apiUrl } from '../ApiConfig/apiConfig.js';

export async function getUserInfo(userId) {
  const token = sessionStorage.getItem("assetsToken");
  try {
    const response = await fetch(`${apiUrl}/user/${userId}`, {
      headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `${token}`
      },
      mode: "cors",
      method: 'GET'
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const userInfo = await response.json();
    return userInfo.Response;
  } catch (error) {
    console.error('Error fetching user information:', error);
    throw error; // Re-throw the error so the calling code can handle it if needed
  }
}
