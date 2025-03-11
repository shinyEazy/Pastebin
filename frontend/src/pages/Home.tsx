import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="home-page">
      <h1>Share Code Snippets Instantly</h1>
      <Link to="/create" className="cta-button">
        Create New Paste
      </Link>
    </div>
  );
};

export default Home;
