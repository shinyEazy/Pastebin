import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PasteEditor from "../components/PasteEditor/Editor";
import usePaste from "../hooks/usePaste";
import Button from "../components/common/Button";

const LANGUAGE_OPTIONS = [
  "Plaintext",
  "Python",
  "JavaScript",
  "HTML",
  "CSS",
  "SQL",
];

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
  const [expiration, setExpiration] = useState("Never");
  const [language, setLanguage] = useState("plaintext");

  const handleSubmit = async () => {
    if (!content.trim()) {
      alert("Content cannot be empty!");
      return;
    }
    try {
      const id = await createPaste(content, expiration, language);
      navigate(`/paste/${id}`);
    } catch (error) {
      console.error("Failed to create paste:", error);
    }
  };

  return (
    <div
      className={`p-6 rounded-lg shadow-md col-span-1 md:col-span-2 ${"bg-white"}`}
    >
      <h2 className="text-xl font-semibold mb-4">New Paste</h2>

      <div className={`border rounded-md overflow-hidden ${"border-gray-200"}`}>
        <PasteEditor content={content} onChange={setContent} />
      </div>

      <div className="mt-4 flex justify-between items-center">
        <div>
          <label
            className={`block text-sm font-medium ${"text-gray-700"} mb-1`}
          >
            Language:
          </label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="rounded-md shadow-sm py-2 px-3 bg-white border border-gray-400 text-gray-900 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
          >
            {LANGUAGE_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            className={`block text-sm font-medium ${"text-gray-700"} mb-1`}
          >
            Paste Expiration:
          </label>
          <select
            value={expiration}
            onChange={(e) => setExpiration(e.target.value)}
            className="rounded-md shadow-sm py-2 px-3 bg-white border border-gray-400 text-gray-900 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
          >
            {EXPIRATION_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <Button
          onClick={handleSubmit}
          loading={loading}
          className={`px-4 py-2 rounded-md font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${""} transition-colors duration-200`}
        >
          Create New Paste
        </Button>
      </div>
    </div>
  );
};

export default CreatePaste;
