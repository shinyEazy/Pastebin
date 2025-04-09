const pool = require("../config/db");

const findUserByUsername = async (username) => {
  const [rows] = await pool.query("SELECT * FROM users WHERE username = ?", [
    username,
  ]);
  return rows[0];
};

const createUser = async (username, password) => {
  await pool.query("INSERT INTO users (username, password) VALUES (?, ?)", [
    username,
    password,
  ]);
};

module.exports = { findUserByUsername, createUser };
