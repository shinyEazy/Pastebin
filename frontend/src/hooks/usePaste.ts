import { useState } from "react";
import { savePaste } from "../services/pasteService";

const usePaste = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createPaste = async (
    content: string,
    expiration: string,
    language: string
  ): Promise<string> => {
    setLoading(true);
    setError(null);

    try {
      const response = await savePaste(content, expiration, language);
      console.log("usePaste received paste:", response);
      return response.id;
    } catch (err: any) {
      const errorMessage =
        err.message || "Failed to save paste. Please try again.";
      setError(errorMessage);
      console.error("usePaste error:", errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { createPaste, loading, error };
};

export default usePaste;
