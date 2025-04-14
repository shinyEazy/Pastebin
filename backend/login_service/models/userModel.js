const express = require("express");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const cors = require("cors");
const db = require("../config/db");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());

const SECRET = "secret-key"; // hoặc từ biến môi trường

// Đăng ký
app.post("/api/register", async (req, res) => {
  const { username, password } = req.body;
  const hashed = await bcrypt.hash(password, 10);

  db.query(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    [username, hashed],
    (err) => {
      if (err)
        return res.status(500).json({ message: "Tên người dùng đã tồn tại" });
      res.json({ message: "Đăng ký thành công" });
    }
  );
});

// Đăng nhập
app.post("/api/login", (req, res) => {
  const { username, password } = req.body;

  db.query(
    "SELECT * FROM users WHERE username = ?",
    [username],
    async (err, results) => {
      if (err || results.length === 0)
        return res.status(401).json({ message: "Sai thông tin" });

      const user = results[0];
      const match = await bcrypt.compare(password, user.password);

      if (match) {
        const token = jwt.sign(
          { id: user.id, username: user.username },
          SECRET,
          { expiresIn: "1h" }
        );
        res.json({ token });
      } else {
        res.status(401).json({ message: "Sai mật khẩu" });
      }
    }
  );
});

// Middleware xác thực
const authMiddleware = (req, res, next) => {
  const token = req.headers["authorization"];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// Trang chủ được bảo vệ
// app.get("/api/home", authMiddleware, (req, res) => {
//   res.json({ message: `Xin chào ${req.user.username}` });
// });

app.listen(5001, () => console.log("🟢 Backend chạy ở http://localhost:3001"));
