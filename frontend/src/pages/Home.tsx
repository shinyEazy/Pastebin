import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  return (
    <div className="home-page">
      <button
        className={`px-4 py-2 rounded-md font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${""} transition-colors duration-200`}
        onClick={() => navigate("/create")}
        style={{ cursor: "pointer" }}
      >
        New Paste
      </button>
    </div>
  );
};

export default Home;
