import axios from "axios";

const API_BASE = "http://localhost";

export interface PasteResponse {
  id: string;
  content: string;
  language: string;
  created_at: string;
  expiration: string;
  views: number;
  is_active: boolean;
  user_id?: string;
}

export const savePaste = async (
  content: string,
  expiration: string,
  language: string
) => {
  try {
    const token = localStorage.getItem("token");
    console.log("Sending token:", token);
    const headers: { [key: string]: string } = {
      "Content-Type": "application/json",
    };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    const response = await axios.post(
      `${API_BASE}/paste/pastes`,
      {
        content,
        expiration,
        language: language.toLowerCase(),
      },
      { headers }
    );
    return response.data;
  } catch (error: any) {
    console.error(
      "Failed to save paste:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.detail || "Failed to save paste");
  }
};

export const getPaste = async (id: string) => {
  try {
    const response = await axios.get(`${API_BASE}/paste/pastes/${id}`);
    return response.data;
  } catch (error: any) {
    console.error(
      "Failed to get paste:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.detail || "Failed to get paste");
  }
};

export const getUserPastes = async () => {
  try {
    const token = localStorage.getItem("token");
    console.log("Sending token for user pastes:", token);
    if (!token) {
      throw new Error("Not authenticated");
    }
    const response = await axios.get(`${API_BASE}/user/pastes`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log("Fetched user pastes:", response.data);
    return response.data;
  } catch (error: any) {
    console.error(
      "Failed to fetch user pastes:",
      error.response?.data || error.message
    );
    throw new Error(
      error.response?.data?.detail || "Failed to fetch user pastes"
    );
  }
};
