import { useState, useEffect } from "react";
import { getUserPastes } from "../services/pasteService";
import { PasteResponse } from "../services/pasteService";
import { Typography } from "@mui/material";
import { Link } from "react-router-dom";

const MyPastes = () => {
  const [pastes, setPastes] = useState<PasteResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPastes = async () => {
      try {
        const userPastes = await getUserPastes();

        console.log("Fetched user pastes:", userPastes);
        setPastes(userPastes);
      } catch (err: any) {
        setError(err.message || "Failed to fetch pastes. Please try again.");
        console.error("Error fetching pastes:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchPastes();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <Typography variant="h4" className="mb-6 text-gray-900 font-bold">
        My Pastes
      </Typography>
      {loading && <Typography className="text-gray-600">Loading...</Typography>}
      {error && <Typography className="text-red-500 mb-4">{error}</Typography>}
      {!loading && !error && pastes.length === 0 && (
        <Typography className="text-gray-600">
          You haven't created any pastes yet.
        </Typography>
      )}
      <div className="grid gap-4">
        {pastes.map((paste) => (
          <div
            key={paste.id}
            className="p-4 bg-white border border-gray-200 rounded-md shadow-sm hover:shadow-md transition-shadow"
          >
            <Link to={`/paste/${paste.id}`}>
              <Typography
                className="text-blue-600 hover:underline font-medium"
                style={{ fontFamily: "monospace" }}
              >
                Paste {paste.id}
              </Typography>
            </Link>
            <Typography
              className="text-gray-600 mt-1 truncate"
              style={{ fontFamily: "monospace" }}
            >
              {paste.content.substring(0, 100)}
              {paste.content.length > 100 ? "..." : ""}
            </Typography>
            <Typography
              className="text-gray-500 text-sm mt-1"
              style={{ fontFamily: "monospace" }}
            >
              Language: {paste.language} | Created:{" "}
              {new Date(paste.created_at).toLocaleString()} | Views:{" "}
              {paste.views}
            </Typography>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyPastes;
