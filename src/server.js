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





const express = require("express");
const app = express();
const cors = require("cors");
require("dotenv").config();
const cookieParser = require("cookie-parser");
const path = require("path");

/* ---------------------------------------------------
   ✅ CORS (JWT HEADER BASED — VERCEL + LOCAL SAFE)
--------------------------------------------------- */

const corsOptions = {
  origin: function (origin, callback) {
    // Allow server-to-server & Postman
    if (!origin) return callback(null, true);

    // Localhost
    if (origin.startsWith("http://localhost")) {
      return callback(null, true);
    }

    // All Vercel preview + production URLs
    if (origin.endsWith(".vercel.app")) {
      return callback(null, true);
    }

    return callback(new Error(`CORS blocked: ${origin}`));
  },
  credentials: false, // 🔥 IMPORTANT: JWT via Authorization header
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
};

app.use(cors(corsOptions));

/* ---------------------------------------------------
   ✅ STATIC FILES
--------------------------------------------------- */

app.use("/uploads", express.static(path.join(__dirname, "uploads")));

/* ---------------------------------------------------
   ✅ BODY PARSERS
--------------------------------------------------- */

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));

// Cookie parser kept (safe even if unused)
app.use(cookieParser());

/* ---------------------------------------------------
   ✅ DATABASE
--------------------------------------------------- */

const connectDB = require("./config/db");
connectDB();

/* ---------------------------------------------------
   ✅ ROUTES
--------------------------------------------------- */

app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/user", require("./routes/userRoutes"));
app.use("/api/resume", require("./routes/resumeRoutes"));
app.use("/api/roadmap", require("./routes/roadmapRoutes"));
app.use("/api", require("./routes/skillGapRoutes"));
app.use("/api/interview", require("./routes/interviewRoutes"));
app.use("/api/settings", require("./routes/settingsRoutes"));
app.use("/api/trends", require("./routes/trendRoutes"));
app.use("/api/dashboard", require("./routes/dashboardRoutes"));

/* ---------------------------------------------------
   ✅ HEALTH CHECK
--------------------------------------------------- */

app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "CarrierCopilot backend running 🚀",
    env: process.env.NODE_ENV || "development",
  });
});

/* ---------------------------------------------------
   ✅ START SERVER
--------------------------------------------------- */

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
