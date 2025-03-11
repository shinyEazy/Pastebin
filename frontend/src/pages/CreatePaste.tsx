import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PasteEditor from "../components/PasteEditor/Editor";
import usePaste from "../hooks/usePaste";
import Button from "../components/common/Button";

const CreatePaste = () => {
  const navigate = useNavigate();
  const { createPaste, loading } = usePaste();
  const [content, setContent] = useState("");

  const handleSubmit = async () => {
    try {
      const id = await createPaste(content);
      navigate(`/paste/${id}`);
    } catch (error) {
      console.error("Failed to create paste:", error);
    }
  };

  return (
    <div className="create-paste-page">
      <h2>Create New Paste</h2>
      <PasteEditor content={content} onChange={setContent} />
      <div className="action-bar">
        <Button onClick={handleSubmit} loading={loading}>
          Save Paste
        </Button>
      </div>
    </div>
  );
};

export default CreatePaste;
