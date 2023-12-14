
/*
    This module encapsulates fetching user information 
*/
import { apiUrl } from '../ApiConfig/apiConfig.js';

export async function getUserInfo(userId) {
  try {
    const response = await fetch(`${apiUrl}/user/${userId}`, {
      method: 'GET',
      mode: 'cors',
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
