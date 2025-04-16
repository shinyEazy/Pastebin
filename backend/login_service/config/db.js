// login_service/config/db.js
const mysql = require("mysql2");
const RETRY_INTERVAL = 10000;

const connection = mysql.createConnection({
  host: process.env.DB_HOST || "db",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD || "123456",
  database: process.env.DB_NAME || "pastebin",
  port: process.env.DB_PORT || 3306,
});

connection.connect((err) => {
  if (err) {
    console.error("MySQL connection error:", err);
    console.log(`Retrying in ${RETRY_INTERVAL / 1000}s...`);
    setTimeout(connectWithRetry, RETRY_INTERVAL);
  } else {
    console.log("Connected to MySQL from login_service 🚀");
  }
});

module.exports = connection;
