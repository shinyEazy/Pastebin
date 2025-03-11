import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:3001/api";

export interface PasteResponse {
  id: string;
  content: string;
  created_at: string;
  expire_at?: string;
}

export const savePaste = async (content: string, expireAt?: string) => {
  const response = await axios.post<PasteResponse>(`${API_BASE}/pastes`, {
    content,
    expire_at: expireAt,
  });
  return response.data;
};

export const getPaste = async (id: string) => {
  const response = await axios.get<PasteResponse>(`${API_BASE}/pastes/${id}`);
  return response.data;
};
