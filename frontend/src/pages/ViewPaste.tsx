import { useEffect, useRef, useState } from "react";
import { useLoaderData } from "react-router-dom";
import { getPaste } from "../services/pasteService";
import type { Paste } from "../types/paste.types";

const ViewPaste = () => {
  const { pasteId } = useLoaderData() as { pasteId: string };
  const [paste, setPaste] = useState<Paste | null>(null);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    const loadPaste = async () => {
      try {
        const pasteData = await getPaste(pasteId);
        const createdAt = new Date(pasteData.created_at);

        setPaste({
          id: pasteData.id,
          content: pasteData.content,
          created_at: createdAt,
          expiration: pasteData.expiration,
          views: pasteData.views,
          is_active: pasteData.is_active,
        });
      } catch (error) {
        console.error("Failed to load paste:", error);
      }
    };

    loadPaste();
  }, [pasteId]);

  if (!paste)
    return (
      <div>
        This page is no longer available. It has either expired, been removed by
        its creator, or removed by one of the Pastebin staff.
      </div>
    );

  return (
    <div className="view-paste-page">
      <pre className="paste-content">{paste.content}</pre>
      <div className="paste-meta">
        <span>
          Created:
          {paste.created_at.toLocaleString("en-GB", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false,
          })}
        </span>
      </div>
      <div className="paste-meta">
        <span>Views: {paste.views}</span>
      </div>
    </div>
  );
};

export default ViewPaste;
