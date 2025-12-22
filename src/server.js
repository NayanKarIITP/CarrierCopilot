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
const path = require("path");
require("dotenv").config();

const app = express();

/* ------------------ CORS ------------------ */
app.use(
  cors({
    origin: [
      "http://localhost:3000",
      "http://localhost:5173",
      /\.vercel\.app$/,
    ],
    credentials: true,
  })
);

/* ------------------ BODY ------------------ */
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true }));

app.use(cookieParser());

/* ------------------ STATIC ------------------ */
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

/* ------------------ DB ------------------ */
require("./config/db")();

/* ------------------ ROUTES ------------------ */
app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/user", require("./routes/userRoutes"));
app.use("/api/resume", require("./routes/resumeRoutes"));
app.use("/api/interview", require("./routes/interviewRoutes"));
app.use("/api/roadmap", require("./routes/roadmapRoutes"));
app.use("/api/settings", require("./routes/settingsRoutes"));
app.use("/api/trends", require("./routes/trendRoutes"));
app.use("/api/dashboard", require("./routes/dashboardRoutes"));

/* ------------------ HEALTH ------------------ */
app.get("/", (_, res) => {
  res.json({ success: true, message: "Backend running 🚀" });
});

/* ------------------ START ------------------ */
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Backend running on port ${PORT}`);
});
