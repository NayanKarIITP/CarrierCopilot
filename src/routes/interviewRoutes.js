// const express = require("express");
// const router = express.Router();
// const auth = require("../middleware/authMiddleware");
// const pythonService = require("../services/pythonService");


// const {
//   getQuestion,
//   analyze,
//   listSessions
// } = require("../controllers/interviewController");

// // Get new interview question
// router.get("/question", getQuestion);

// // Analyze interview (frame/voice/transcript)
// router.post("/analyze", auth, analyze);

// // List stored sessions
// router.get("/sessions", auth, listSessions);

// // NEW: frame metrics
// router.post("/frame-metrics", auth, async (req, res) => {
//   try {
//     const { image_base64 } = req.body;
//     if (!image_base64) {
//       return res.status(400).json({ success: false, message: "image_base64 required" });
//     }

//     const metrics = await pythonService.getFrameMetrics(image_base64);
//     return res.json({ success: true, metrics });
//   } catch (err) {
//     console.error("Frame metrics error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// });

// module.exports = router;






const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");

const {
  startSession,
  getQuestion,
  analyze,
  listSessions,
  getFrameMetrics // ✅ Added this
} = require("../controllers/interviewController");

// Start a new session
router.post("/start", auth, startSession);

// Get next question (Changed to POST to accept session ID/Role)
router.post("/next-question", auth, getQuestion);

// Analyze interview (frame/voice/transcript)
router.post("/analyze", auth, analyze);

// List stored sessions
router.get("/sessions", auth, listSessions);

// Frame metrics (Video Feed calls this)
router.post("/frame-metrics", auth, getFrameMetrics);

module.exports = router;