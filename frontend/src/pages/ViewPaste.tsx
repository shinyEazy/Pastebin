import { useEffect, useRef, useState } from "react";
import { useLoaderData } from "react-router-dom";
import { getPaste } from "../services/pasteService";
import type { Paste } from "../types/paste.types";
import { useNavigate } from "react-router-dom";

const ViewPaste = () => {
  const { pasteId } = useLoaderData() as { pasteId: string };
  const [paste, setPaste] = useState<Paste | null>(null);
  const didFetch = useRef(false);
  const navigate = useNavigate();

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
          language: pasteData.language,
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
      <div
        className={`p-6 rounded-lg shadow-md col-span-1 md:col-span-2 ${"bg-white"}`}
      >
        This page is no longer available. It has either expired, been removed by
        its creator, or removed by one of the Pastebin staff.
      </div>
    );

  return (
    <div
      className={`p-6 rounded-lg shadow-md col-span-1 md:col-span-2 ${"bg-white"}`}
    >
      <div className="flex justify-between items-center mb-4">
        <button
          className={`px-3 py-1 text-sm rounded-md font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${""} transition-colors duration-200`}
          onClick={() => navigate("/create")}
          style={{ cursor: "pointer" }}
        >
          New Paste
        </button>
      </div>
      <div
        className={`rounded-md overflow-hidden ${"bg-gray-50"} shadow-inner`}
      >
        <pre
          className={`p-4 font-mono text-sm whitespace-pre-wrap ${"text-gray-800"}`}
        >
          {paste.content}
        </pre>
      </div>
      <div
        className={`mt-4 flex space-x-4 ${"text-gray-500"} text-sm`}
        style={{ display: "flex", flexDirection: "column" }}
      >
        <div>Created: {paste?.created_at.toLocaleString()}</div>
        <div style={{ margin: 0 }}>Language: {paste?.language}</div>
        <div style={{ margin: 0 }}>Views: {paste?.views}</div>
        <div style={{ margin: 0 }}>Expires: {paste?.expiration}</div>
      </div>
    </div>
  );
};

export default ViewPaste;
