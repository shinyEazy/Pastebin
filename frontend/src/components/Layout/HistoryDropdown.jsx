import { useState, useEffect } from "react";
import axios from "axios";
const HistoryDropdown = () => {
  const [pastes, setPastes] = useState([]);
  const [isHover, setIsHover] = useState(false);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/user-pastes", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((res) => {
        console.log("📦 API trả về:", res.data);
        setPastes(res.data);
      })
      .catch((err) => {
        console.error("Lỗi khi gọi API:", err);
        setPastes([]);
      });
  }, []);

  return (
    <div
      onMouseEnter={() => setIsHover(true)}
      onMouseLeave={() => setIsHover(false)}
      className="relative"
    >
      <button className="px-4 py-2 bg-gray-200 rounded">📜 History</button>

      {isHover && (
        <div className="absolute z-10 top-full mt-2 w-64 max-h-60 overflow-y-auto bg-white border rounded shadow-lg">
          {pastes.length === 0 ? (
            <div className="p-4 text-gray-500">No pastes yet</div>
          ) : (
            pastes.map((url, index) => {
              const pasteId = url.split("/").pop();
              return (
                <a
                  key={index}
                  href={`/paste/${pasteId}`}
                  className="block px-4 py-2 hover:bg-gray-100 text-sm text-blue-600"
                >
                  {`Paste #${pasteId}`}
                </a>
              );
            })
          )}
        </div>
      )}
    </div>
  );
};

export default HistoryDropdown;
