// const express = require("express");
// const app = express();
// const cors = require("cors");
// require("dotenv").config();
// const cookieParser = require("cookie-parser");

// // -----------------------------
// // CORS (must be FIRST)
// // -----------------------------
// app.use(
//   cors({
//     origin: "http://localhost:3000",
//     credentials: true,
//   })
// );

// // -----------------------------
// // Core Middlewares
// // -----------------------------
// app.use(express.json({ limit: "10mb" }));
// app.use(cookieParser());

// // -----------------------------
// // Database
// // -----------------------------
// const connectDB = require("./config/db");
// connectDB();

// // -----------------------------
// // Routes
// // -----------------------------
// app.use("/api/auth", require("./routes/authRoutes"));
// app.use("/api/resume", require("./routes/resumeRoutes"));
// app.use("/api/roadmap", require("./routes/roadmapRoutes"));
// app.use("/api", require("./routes/skillGapRoutes"));
// app.use("/api/interview", require("./routes/interviewRoutes"));
// app.use("/api/settings", require("./routes/settingsRoutes"));
// app.use("/api/trends", require("./routes/trendRoutes"));
// app.use("/api/dashboard", require("./routes/dashboardRoutes"));

// // -----------------------------
// // Server Start
// // -----------------------------
// app.listen(5000, () => console.log("🔥 Server running on port 5000"));




// src/server.js
const express = require("express");
const cors = require("cors");
const cookieParser = require("cookie-parser");
require("dotenv").config();

const app = express();

/* ---------------- CORS ---------------- */
app.use(
  cors({
    origin: (origin, cb) => cb(null, true),
    credentials: true,
  })
);

/* ❗ DO NOT PARSE JSON BEFORE MULTER ROUTES */
app.use(cookieParser());

/* ---------------- ROUTES ---------------- */
app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/user", require("./routes/userRoutes"));
app.use("/api/resume", require("./routes/resumeRoutes")); // ⬅ multer lives here
app.use("/api/interview", require("./routes/interviewRoutes"));
app.use("/api/roadmap", require("./routes/roadmapRoutes"));
app.use("/api/trends", require("./routes/trendRoutes"));

/* ---------------- JSON PARSER (AFTER) ---------------- */
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true }));

/* ---------------- HEALTH ---------------- */
app.get("/", (_, res) => res.json({ ok: true }));

/* ---------------- ERROR HANDLER (CRITICAL) ---------------- */
app.use((err, req, res, next) => {
  console.error("🔥 GLOBAL ERROR:", err.message);
  res.status(400).json({ success: false, message: err.message });
});

app.listen(process.env.PORT || 5000, () =>
  console.log("🚀 Backend running")
);
