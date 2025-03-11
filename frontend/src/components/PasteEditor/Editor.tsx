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
        className="w-full min-h-64 p-4 font-mono text-sm bg-gray-50 text-gray-800 focus:outline-none transition-colors duration-200"
      />
    </div>
  );
};

export default PasteEditor;
