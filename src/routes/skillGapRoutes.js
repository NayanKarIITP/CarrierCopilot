const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");
const pythonService = require("../services/pythonService");

router.post("/skill-gap", auth, async (req, res) => {
  try {
    const { resumeSkills, targetRole } = req.body;

    const result = await pythonService.skillGapAnalyzer(resumeSkills, targetRole);

    return res.json({ success: true, data: result });

  } catch (err) {
    console.error("Skill gap error:", err);
    return res.status(500).json({ success: false, message: "AI skill gap analysis failed" });
  }
});

module.exports = router;
