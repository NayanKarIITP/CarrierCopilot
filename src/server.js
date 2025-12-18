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
   ✅ CORS CONFIG (VERCEL + LOCAL + PREVIEW SUPPORT)
--------------------------------------------------- */

const allowedOrigins = [
  "http://localhost:3000",
  "http://localhost:5173",
  "https://carrier-copilot.vercel.app",
  "https://carrier-copilot-dl8qczfgk-nayankariitps-projects.vercel.app/",
];

app.use(
  cors({
    origin: function (origin, callback) {
      // Allow requests without origin (Postman, server-to-server)
      if (!origin) return callback(null, true);

      if (allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error(`CORS blocked: ${origin}`));
      }
    },
    credentials: true,
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization"],
  })
);

// ⚠️ REQUIRED for preflight requests
app.options("*", cors());

/* ---------------------------------------------------
   ✅ STATIC FILES
--------------------------------------------------- */

const uploadsPath = path.join(__dirname, "uploads");
app.use("/uploads", express.static(uploadsPath));

/* ---------------------------------------------------
   ✅ BODY PARSING
--------------------------------------------------- */

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));
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
   ✅ HEALTH CHECK (IMPORTANT FOR RENDER)
--------------------------------------------------- */

app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Career Copilot Backend is running 🚀",
  });
});

/* ---------------------------------------------------
   ✅ SERVER START (RENDER COMPATIBLE)
--------------------------------------------------- */

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});

