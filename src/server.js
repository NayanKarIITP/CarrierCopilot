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

// 1. CORS Configuration
app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
  })
);

// 2. Serve Static Files (Uploads)
const uploadsPath = path.join(__dirname, "uploads");
console.log("📂 Serving uploads from:", uploadsPath);
app.use("/uploads", express.static(uploadsPath));

// 3. ✅ FIX: Increase Limits for Image Uploads (JSON & URL Encoded)
app.use(express.json({ limit: "50mb" })); // Increased to 50mb to be safe
app.use(express.urlencoded({ limit: "50mb", extended: true }));

app.use(cookieParser());

// 4. Database Connection
const connectDB = require("./config/db");
connectDB();

// 5. Routes
app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/user", require("./routes/userRoutes"));
app.use("/api/resume", require("./routes/resumeRoutes"));
app.use("/api/roadmap", require("./routes/roadmapRoutes"));
app.use("/api", require("./routes/skillGapRoutes"));
app.use("/api/interview", require("./routes/interviewRoutes"));
app.use("/api/settings", require("./routes/settingsRoutes"));
app.use("/api/trends", require("./routes/trendRoutes"));
app.use("/api/dashboard", require("./routes/dashboardRoutes"));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));