import { useState } from "react";
import { savePaste } from "../services/pasteService";

const usePaste = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createPaste = async (content: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await savePaste(content);
      return response.id;
    } catch (err) {
      setError("Failed to save paste. Please try again.");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { createPaste, loading, error };
};

export default usePaste;
