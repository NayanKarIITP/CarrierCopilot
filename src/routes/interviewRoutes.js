const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");

const {
  getQuestion,
  analyze,
  listSessions
} = require("../controllers/interviewController");

// Get new interview question
router.get("/question", getQuestion);

// Analyze interview (frame/voice/transcript)
router.post("/analyze", auth, analyze);

// List stored sessions
router.get("/sessions", auth, listSessions);

module.exports = router;
