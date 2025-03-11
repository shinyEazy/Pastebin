import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="app-header">
      <nav>
        <Link to="/" className="logo">
          PasteBin
        </Link>
        <div className="nav-links">
          <Link to="/create">New Paste</Link>
        </div>
      </nav>
    </header>
  );
};

export default Header;
