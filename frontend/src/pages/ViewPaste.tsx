import { useEffect, useState } from "react";
import { useLoaderData } from "react-router-dom";
import { getPaste } from "../services/pasteService";
import type { Paste } from "../types/paste.types";

const ViewPaste = () => {
  const { pasteId } = useLoaderData() as { pasteId: string };
  const [paste, setPaste] = useState<Paste | null>(null);

  useEffect(() => {
    const loadPaste = async () => {
      try {
        const pasteData = await getPaste(pasteId);
        setPaste({
          ...pasteData,
          createdAt: new Date(pasteData.createdAt),
          expiresAt: pasteData.expiresAt
            ? new Date(pasteData.expiresAt)
            : undefined,
        });
      } catch (error) {
        console.error("Failed to load paste:", error);
      }
    };

    loadPaste();
  }, [pasteId]);

  if (!paste) return <div>Loading...</div>;

  return (
    <div className="view-paste-page">
      <pre className="paste-content">{paste.content}</pre>
      <div className="paste-meta">
        <span>Created: {new Date(paste.createdAt).toLocaleString()}</span>
        {paste.language && <span>Language: {paste.language}</span>}
      </div>
    </div>
  );
};

export default ViewPaste;
