import { Box, Popover, Typography, Link } from "@mui/material";
import { Button, Avatar, Menu, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import React, { useContext } from "react";
import { useState } from "react";
import { UserContext } from "src/users/userContext";
import HistoryDropdown from "./HistoryDropdown";

const Header = () => {
  const navigate = useNavigate();
  const { user, logout } = useContext(UserContext);
  const [anchorEl, setAnchorEl] = useState<HTMLDivElement | null>(null);
  const [anchorHistory, setAnchorHistory] = useState<HTMLLIElement | null>(
    null
  );
  const [openHistoryPopover, setOpenHistoryPopover] = useState(false);

  const handleAvatarClick = (event: React.MouseEvent<HTMLDivElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleClose();
    navigate("/");
  };

  function handleHistory(
    event: React.MouseEvent<HTMLLIElement, MouseEvent>
  ): void {
    setAnchorHistory(event.currentTarget);
    setOpenHistoryPopover(true);
  }

  const handleCloseHistoryPopover = () => {
    setAnchorHistory(null);
    setOpenHistoryPopover(false);
  };

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
                      component="div"
                      onClick={handleAvatarClick}
                      style={{ cursor: "pointer" }}
                    />
                    <Menu
                      anchorEl={anchorEl}
                      open={Boolean(anchorEl)}
                      onClose={handleClose}
                    >
                      <MenuItem onClick={handleLogout}>Log out</MenuItem>
                    </Menu>
                    <HistoryDropdown />
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
