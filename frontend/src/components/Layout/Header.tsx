import { Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className={`sticky top-0 z-10 ${"bg-white"} shadow-sm`}>
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <span
                className="text-xl font-bold text-blue-600"
                onClick={() => navigate("/")}
                style={{ cursor: "pointer" }}
              >
                PasteBin
              </span>
            </div>
            <nav className="ml-6 flex items-center space-x-4">
              <Typography
                className={`px-3 py-2 rounded-md text-sm font-medium ${"text-gray-700 hover:bg-gray-100"}`}
                onClick={() => navigate("/")}
                style={{ cursor: "pointer", fontFamily: "monospace" }}
              >
                Home
              </Typography>
              <Typography
                className={`px-3 py-2 rounded-md text-sm font-medium ${"text-gray-700 hover:bg-gray-100"}`}
                onClick={() => navigate("/create")}
                style={{ cursor: "pointer", fontFamily: "monospace" }}
              >
                New Paste
              </Typography>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
