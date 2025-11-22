const path = require("path");
const fs = require("fs");
const Resume = require("../models/Resume");
const User = require("../models/user");
const pythonService = require("../services/pythonService");

/**
 * Upload resume file (multer must populate req.file) and process with Python microservice.
 * - Saves parsed data as Resume document
 * - Updates User with resume metadata (score, skills, flags)
 */
exports.uploadResume = async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: "No file uploaded" });

    const filePath = req.file.path;
    const filename = req.file.filename;
    const targetRole = req.body.targetRole || "senior-fullstack";

    // call python microservice to parse and analyze
    const pythonResult = await pythonService.processResume(filePath, filename, targetRole);

    // create Resume document
    const resumeDoc = await Resume.create({
      userId: req.user ? req.user._id : null,
      rawText: pythonResult.raw_text || pythonResult.parsed?.raw_text || "",
      skills: pythonResult.parsed?.skills || pythonResult.skills || [],
      education: pythonResult.parsed?.education || pythonResult.education || [],
      experience: pythonResult.parsed?.experience || pythonResult.experience || [],
      score: pythonResult.resume_score || null,
      feedback: pythonResult.suggestions || pythonResult.feedback || [],
      fileURL: `/uploads/resumes/${filename}`,
    });

    // update User summary fields (if user logged in)
    if (req.user) {
      await User.findByIdAndUpdate(req.user._id, {
        resumeUploaded: true,
        resumeScore: pythonResult.resume_score || null,
        extractedSkills: pythonResult.parsed?.skills || pythonResult.skills || [],
        skillGaps: (pythonResult.skill_gaps || []).map((g) => g.skill || g),
      });
    }

    return res.json({
      success: true,
      data: {
        resume: resumeDoc,
        analysis: pythonResult,
        pdf_url: `/uploads/resumes/${filename}`,
      },
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error", details: err.message });
  }
};

// Get resumes for a user (protected)
exports.listUserResumes = async (req, res) => {
  try {
    const userId = req.user._id;
    const resumes = await Resume.find({ userId }).sort({ createdAt: -1 });
    return res.json({ success: true, data: resumes });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// Get single resume by id
exports.getResume = async (req, res) => {
  try {
    const resume = await Resume.findById(req.params.id);
    if (!resume) return res.status(404).json({ success: false, message: "Resume not found" });
    return res.json({ success: true, data: resume });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// Delete resume (protected)
exports.deleteResume = async (req, res) => {
  try {
    const resume = await Resume.findById(req.params.id);
    if (!resume) return res.status(404).json({ success: false, message: "Resume not found" });

    // Confirm ownership if protected
    if (req.user && resume.userId.toString() !== req.user._id.toString()) {
      return res.status(403).json({ success: false, message: "Not authorized" });
    }

    // delete file from disk (best effort)
    if (resume.fileURL) {
      const filePath = path.join(__dirname, "..", "uploads", "resumes", path.basename(resume.fileURL));
      try { if (fs.existsSync(filePath)) fs.unlinkSync(filePath); } catch (e) { /* ignore */ }
    }

    await resume.deleteOne();
    return res.json({ success: true, message: "Resume deleted" });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};
