import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PasteEditor from "../components/PasteEditor/Editor";
import usePaste from "../hooks/usePaste";
import Button from "../components/common/Button";

const EXPIRATION_OPTIONS = [
  "Never",
  "Burn After Read",
  "1 Minute",
  "10 Minutes",
  "1 Hour",
  "1 Day",
  "1 Week",
  "2 Weeks",
  "1 Month",
  "6 Months",
  "1 Year",
];

const CreatePaste = () => {
  const navigate = useNavigate();
  const { createPaste, loading } = usePaste();
  const [content, setContent] = useState("");
  const [expiration, setExpiration] = useState<string | "">("Never");

  const handleSubmit = async () => {
    try {
      if (!content.trim()) {
        alert("Content cannot be empty!");
        return;
      }

      const id = await createPaste(content, expiration);
      navigate(`/paste/${id}`);
    } catch (error) {
      console.error("Failed to create paste:", error);
    }
  };

  return (
    <div className="create-paste-page" style={{ height: "500px" }}>
      <h2>New Paste</h2>
      <PasteEditor content={content} onChange={setContent} />

      <label>Paste Expiration:</label>
      <select
        value={expiration}
        onChange={(e) => setExpiration(e.target.value)}
      >
        {EXPIRATION_OPTIONS.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <div className="action-bar" style={{ marginTop: "8px" }}>
        <Button onClick={handleSubmit} loading={loading}>
          Create New Paste
        </Button>
      </div>
    </div>
  );
};

export default CreatePaste;
