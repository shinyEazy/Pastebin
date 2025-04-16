import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";
const USER_API_BASE =
  process.env.REACT_APP_USER_API_BASE || "http://localhost:8002";

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
): Promise<PasteResponse> => {
  try {
    const token = localStorage.getItem("token");
    console.log("Sending token:", token);
    const headers: { [key: string]: string } = {
      "Content-Type": "application/json",
    };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    const response = await axios.post<PasteResponse>(
      `${API_BASE}/pastes`,
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

export const getPaste = async (id: string): Promise<PasteResponse> => {
  try {
    const response = await axios.get<PasteResponse>(`${API_BASE}/pastes/${id}`);
    return response.data;
  } catch (error: any) {
    console.error(
      "Failed to get paste:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.detail || "Failed to get paste");
  }
};

export const getUserPastes = async (): Promise<PasteResponse[]> => {
  try {
    const token = localStorage.getItem("token");
    console.log("Sending token for user pastes:", token);

    if (!token) {
      throw new Error("Not authenticated");
    }

    const response = await axios.get<PasteResponse[]>(
      `${USER_API_BASE}/user/pastes`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

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
