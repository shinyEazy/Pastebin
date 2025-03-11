import { ChangeEvent } from "react";

interface EditorProps {
  content: string;
  onChange: (content: string) => void;
}

const PasteEditor = ({ content, onChange }: EditorProps) => {
  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
  };

  return (
    <div className="paste-editor">
      <textarea
        value={content}
        onChange={handleChange}
        placeholder="Enter your paste content..."
        rows={5}
      />
    </div>
  );
};

export default PasteEditor;
