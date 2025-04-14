import { Typography } from "@mui/material";
import { Button, Avatar, Menu, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import React, { useContext } from "react";
import { useState } from "react";
import { UserContext } from "src/users/userContext";

const Header = () => {
  const navigate = useNavigate();
  const { user, logout } = useContext(UserContext);
  const [anchorEl, setAnchorEl] = useState(null);

  // const handleAvatarClick = (event: {
  //   currentTarget: React.SetStateAction<null>;
  // }) => {
  //   setAnchorEl(event.currentTarget);
  // };

  // const handleClose = () => {
  //   setAnchorEl(null);
  // };

  // const handleLogout = () => {
  //   logout(); // Gọi hàm logout từ context
  //   handleClose();
  //   navigate("/");
  // };

  return (
    <header className={`sticky top-0 z-10 bg-white shadow-sm `}>
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
              <div className="ml-6 flex items-center space-x-4">
                {user ? (
                  <>
                    <Typography style={{ fontFamily: "monospace" }}>
                      {user.username}
                    </Typography>
                    <Avatar
                      //onClick={handleAvatarClick}
                      style={{ cursor: "pointer" }}
                    />
                    <Menu
                      anchorEl={anchorEl}
                      open={Boolean(anchorEl)}
                      //onClose={handleClose}
                    >
                      {/* <MenuItem onClick={handleLogout}>Đăng xuất</MenuItem> */}
                    </Menu>
                  </>
                ) : (
                  <>
                    <Button
                      variant="contained"
                      className="p-4 m-2"
                      onClick={() => navigate("/login")}
                    >
                      Login
                    </Button>
                    <Button
                      variant="outlined"
                      className="p-4 m-2"
                      onClick={() => navigate("/register")}
                    >
                      Register
                    </Button>
                  </>
                )}
              </div>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
