import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:3001/api";

export interface PasteResponse {
  id: string;
  content: string;
  createdAt: string;
  language?: string;
  expiresAt?: string;
}

export const savePaste = async (content: string) => {
  const response = await axios.post<PasteResponse>(`${API_BASE}/pastes`, {
    content,
  });
  return response.data;
};

export const getPaste = async (id: string) => {
  const response = await axios.get<PasteResponse>(`${API_BASE}/pastes/${id}`);
  return response.data;
};
