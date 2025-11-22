// src/controllers/interviewController.js
const Interview = require("../models/Interview");
const pythonService = require("../services/pythonService");

/**
 * Fetch a new interview question (Python Microservice)
 */
exports.getQuestion = async (req, res) => {
  try {
    const q = await pythonService.getInterviewQuestion();

    return res.json({
      success: true,
      question: q.question,
      follow_up: q.follow_up,
      difficulty: q.difficulty,
    });
  } catch (err) {
    console.error("Interview Question Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

/**
 * Analyze the transcript (answer) of the candidate
 */
exports.analyze = async (req, res) => {
  try {
    console.log("REQ BODY →", req.body);
    const { transcript, question } = req.body;

    if (!transcript) {
      return res
        .status(400)
        .json({ success: false, message: "Transcript is required" });
    }

    // Call Python microservice
    const analysis = await pythonService.analyzeInterview(transcript);

    // Save session ONLY if logged in
    let session = null;
    if (req.user) {
      session = await Interview.create({
        userId: req.user._id,
        question: question || "",
        transcript,
        analysis,
      });
    }

    return res.json({
      success: true,
      data: {
        analysis,
        session,
      },
    });
  } catch (err) {
    console.error("Interview Analysis Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

/**
 * List all interview sessions of logged-in user
 */
exports.listSessions = async (req, res) => {
  try {
    const sessions = await Interview.find({ userId: req.user._id }).sort({
      createdAt: -1,
    });

    return res.json({ success: true, data: sessions });
  } catch (err) {
    console.error("List Sessions Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};
