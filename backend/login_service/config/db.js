const mysql = require("mysql2");

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "123456",
  database: "login_db",
});

db.connect((err) => {
  if (err) throw err;
  console.log("✅ MySQL connected");
});

module.exports = db;
