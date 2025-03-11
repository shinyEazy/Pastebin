import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PasteEditor from "../components/PasteEditor/Editor";
import usePaste from "../hooks/usePaste";
import Button from "../components/common/Button";

const CreatePaste = () => {
  const navigate = useNavigate();
  const { createPaste, loading } = usePaste();
  const [content, setContent] = useState("");
  const [expireAt, setExpireAt] = useState<string | "">("");

  const handleSubmit = async () => {
    let localISO: string | undefined;

    try {
      if (!content.trim()) {
        alert("Content cannot be empty!");
        return;
      }

      if (expireAt) {
        const date = new Date(expireAt);
        const now = new Date();

        if (isNaN(date.getTime())) {
          alert("Invalid expiration time!");
          return;
        }

        if (date <= now) {
          alert("Expiration time must be in the future!");
          return;
        }

        localISO =
          date.getFullYear() +
          "-" +
          String(date.getMonth() + 1).padStart(2, "0") +
          "-" +
          String(date.getDate()).padStart(2, "0") +
          "T" +
          String(date.getHours()).padStart(2, "0") +
          ":" +
          String(date.getMinutes()).padStart(2, "0") +
          ":" +
          String(date.getSeconds()).padStart(2, "0");

        console.log(localISO);
      }

      const id = await createPaste(content, localISO);
      navigate(`/paste/${id}`);
    } catch (error) {
      console.error("Failed to create paste:", error);
    }
  };

  return (
    <div className="create-paste-page">
      <h2>Create New Paste</h2>
      <PasteEditor content={content} onChange={setContent} />

      <label>Expiration Date & Time:</label>
      <input
        type="datetime-local"
        value={expireAt}
        onChange={(e) => setExpireAt(e.target.value)}
      />

      <div className="action-bar">
        <Button onClick={handleSubmit} loading={loading}>
          Save Paste
        </Button>
      </div>
    </div>
  );
};

export default CreatePaste;
