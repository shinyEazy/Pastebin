import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

export interface PasteResponse {
  id: string;
  content: string;
  created_at: string;
  expiration: string;
  views: number;
  is_active: boolean;
}

export const savePaste = async (content: string, expiration: string) => {
  try {
    const response = await axios.post<PasteResponse>(`${API_BASE}/pastes`, {
      content,
      expiration,
    });
    return response.data;
  } catch (error) {
    console.error("Failed to save paste:", error);
    throw error;
  }
};

export const getPaste = async (id: string) => {
  const response = await axios.get<PasteResponse>(`${API_BASE}/pastes/${id}`);
  return response.data;
};
