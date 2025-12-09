
// // src/controllers/resumeController.js

// const path = require("path");
// const fs = require("fs");
// const Resume = require("../models/Resume");
// const User = require("../models/user");
// const pythonService = require("../services/pythonService");

// /**
//  * Upload & Process Resume (FIXED VERSION)
//  * - Works with FastAPI microservice
//  * - Saves Resume document
//  * - Updates User dashboard fields
//  * - Returns score and feedback to frontend
//  */
// exports.uploadResume = async (req, res) => {
//   try {
//     if (!req.file)
//       return res.status(400).json({ success: false, message: "No file uploaded" });

//     const filePath = req.file.path;
//     const filename = req.file.filename;
//     const targetRole = req.body.targetRole || "fullstack-developer";

//     console.log("📤 Sending file to Python service...");

//     // ---- CALL PYTHON ----
//     const result = await pythonService.processResume(filePath, targetRole);

//     if (!result.success) {
//       return res.status(400).json({
//         success: false,
//         message: "Python microservice failed",
//       });
//     }

//     // Parsed Data - check multiple possible locations
//     const parsed = result.parsedResume?.parsed || result.parsedResume || {};
    
//     // Extract score and feedback (might be at different levels)
//     const score = parsed.score || result.score || 0;
//     const feedback = parsed.feedback || result.feedback || [];
//     const skills = parsed.skills || [];
//     const education = parsed.education || [];
//     const experience = parsed.experience || [];

//     console.log("📊 Parsed data:", {
//       score,
//       feedbackCount: feedback.length,
//       skillsCount: skills.length,
//       educationCount: education.length,
//       experienceCount: experience.length
//     });

//     // ---- SAVE RESUME DOCUMENT ----
//     const resumeDoc = await Resume.create({
//       userId: req.user._id,
//       rawText: parsed.raw_text || "",
//       skills: skills,
//       education: education,
//       experience: experience,
//       score: score,
//       feedback: feedback,
//       fileURL: `/uploads/resumes/${filename}`,
//     });

//     // ---- UPDATE USER MODEL ----
//     await User.findByIdAndUpdate(req.user._id, {
//       resumeUploaded: true,
//       resumeScore: score,
//       extractedSkills: skills,
//       skillGaps: parsed.skill_gaps || [],
//       roadmapGenerated: true,
//       roadmap: result.generatedRoadmap || {},
//     });

//     // ---- RETURN COMPLETE DATA TO FRONTEND ----
//     return res.json({
//       success: true,
//       data: {
//         resume: resumeDoc,
//         parsedResume: {
//           skills: skills,
//           education: education,
//           experience: experience,
//           score: score,  // ✅ Now included!
//           feedback: feedback,  // ✅ Now included!
//           raw_text: parsed.raw_text || ""
//         },
//         roadmap: result.generatedRoadmap,
//         pdf_url: `/uploads/resumes/${filename}`,
//       },
//     });

//   } catch (err) {
//     console.error("Upload Resume Error:", err.message);
//     return res.status(500).json({
//       success: false,
//       message: "Server error",
//       details: err.message,
//     });
//   }
// };

// /**
//  * LIST all resumes for logged-in user
//  */
// exports.listUserResumes = async (req, res) => {
//   try {
//     const resumes = await Resume.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: resumes });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * GET single resume
//  */
// exports.getResume = async (req, res) => {
//   try {
//     const resume = await Resume.findById(req.params.id);
//     if (!resume)
//       return res.status(404).json({ success: false, message: "Resume not found" });

//     return res.json({ success: true, data: resume });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * DELETE resume
//  */
// exports.deleteResume = async (req, res) => {
//   try {
//     const resume = await Resume.findById(req.params.id);
//     if (!resume)
//       return res.status(404).json({ success: false, message: "Resume not found" });

//     if (resume.userId.toString() !== req.user._id.toString()) {
//       return res.status(403).json({ success: false, message: "Not authorized" });
//     }

//     // Delete file
//     if (resume.fileURL) {
//       const filePath = path.join(
//         __dirname,
//         "..",
//         "uploads",
//         "resumes",
//         path.basename(resume.fileURL)
//       );

//       try {
//         if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
//       } catch (e) {
//         console.warn("File delete error:", e);
//       }
//     }

//     await resume.deleteOne();
//     return res.json({ success: true, message: "Resume deleted successfully" });

//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };













// // src/controllers/resumeController.js

// const path = require("path");
// const fs = require("fs");
// const Resume = require("../models/Resume");
// const User = require("../models/user");
// const pythonService = require("../services/pythonService");

// /**
//  * Upload & Process Resume (FIXED FOR FEEDBACK)
//  */
// exports.uploadResume = async (req, res) => {
//   try {
//     if (!req.file)
//       return res.status(400).json({ success: false, message: "No file uploaded" });

//     const filePath = req.file.path;
//     const filename = req.file.filename;
//     const targetRole = req.body.targetRole || "fullstack-developer";

//     console.log("📤 Sending file to Python service...");

//     // ---- CALL PYTHON ----
//     const result = await pythonService.processResume(filePath, targetRole);

//     if (!result.success) {
//       return res.status(400).json({
//         success: false,
//         message: "Python microservice failed",
//       });
//     }

//     // ---------------------------------------------------------
//     // ✅ CRITICAL FIX: Robust Data Extraction
//     // ---------------------------------------------------------
    
//     // 1. Identify the main data objects
//     // The Python script returns { parsed: {...}, analysis: {...} }
//     // Sometimes it's nested inside 'parsedResume' depending on pythonService.js
//     const rootData = result.parsedResume || result;
//     const parsedObj = rootData.parsed || rootData || {};
//     const analysisObj = rootData.analysis || {};

//     // 2. Extract Score (Prioritize Analysis, fallback to Parsed)
//     const score = analysisObj.resume_score || parsedObj.score || result.score || 0;

//     // 3. Extract Feedback (The most common point of failure)
//     // We check ALL valid locations where feedback might be hiding.
//     let feedback = [];
    
//     if (analysisObj.feedback && analysisObj.feedback.length > 0) {
//         feedback = analysisObj.feedback;
//     } 
//     else if (analysisObj.high_level_feedback && analysisObj.high_level_feedback.length > 0) {
//         feedback = analysisObj.high_level_feedback;
//     }
//     else if (parsedObj.feedback && parsedObj.feedback.length > 0) {
//         feedback = parsedObj.feedback;
//     }
//     else if (parsedObj.high_level_feedback && parsedObj.high_level_feedback.length > 0) {
//         feedback = parsedObj.high_level_feedback;
//     }

//     // 4. Extract Standard Fields
//     const skills = parsedObj.skills || [];
//     const education = parsedObj.education || [];
//     const experience = parsedObj.experience || [];

//     console.log("📊 Parsed Data Summary:", {
//       score,
//       feedbackItems: feedback.length, // This should now be > 0
//       skillsFound: skills.length
//     });

//     // ---- SAVE RESUME DOCUMENT ----
//     const resumeDoc = await Resume.create({
//       userId: req.user._id,
//       rawText: parsedObj.raw_text || "",
//       skills: skills,
//       education: education,
//       experience: experience,
//       score: score,
//       feedback: feedback, // Saving the correctly found feedback
//       fileURL: `/uploads/resumes/${filename}`,
//     });

//     // ---- UPDATE USER MODEL ----
//     await User.findByIdAndUpdate(req.user._id, {
//       resumeUploaded: true,
//       resumeScore: score,
//       extractedSkills: skills,
//       skillGaps: parsedObj.skill_gaps || [],
//       roadmapGenerated: true,
//       roadmap: result.generatedRoadmap || {},
//     });

//     // ---- RETURN COMPLETE DATA TO FRONTEND ----
//     return res.json({
//       success: true,
//       data: {
//         resume: resumeDoc,
//         parsedResume: {
//           skills: skills,
//           education: education,
//           experience: experience,
//           score: score,
//           feedback: feedback, // Sending it to frontend
//           high_level_feedback: feedback, // Dual-support for frontend
//           raw_text: parsedObj.raw_text || ""
//         },
//         roadmap: result.generatedRoadmap,
//         pdf_url: `/uploads/resumes/${filename}`,
//       },
//     });

//   } catch (err) {
//     console.error("Upload Resume Error:", err.message);
//     return res.status(500).json({
//       success: false,
//       message: "Server error",
//       details: err.message,
//     });
//   }
// };

// // ... (Keep the other functions: listUserResumes, getResume, deleteResume exactly as they were) ...
// exports.listUserResumes = async (req, res) => {
//   try {
//     const resumes = await Resume.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: resumes });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// exports.getResume = async (req, res) => {
//   try {
//     const resume = await Resume.findById(req.params.id);
//     if (!resume)
//       return res.status(404).json({ success: false, message: "Resume not found" });
//     return res.json({ success: true, data: resume });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// exports.deleteResume = async (req, res) => {
//   try {
//     const resume = await Resume.findById(req.params.id);
//     if (!resume) return res.status(404).json({ success: false, message: "Resume not found" });

//     if (resume.userId.toString() !== req.user._id.toString()) {
//       return res.status(403).json({ success: false, message: "Not authorized" });
//     }

//     if (resume.fileURL) {
//       const filePath = path.join(__dirname, "..", "uploads", "resumes", path.basename(resume.fileURL));
//       try {
//         if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
//       } catch (e) {
//         console.warn("File delete error:", e);
//       }
//     }

//     await resume.deleteOne();
//     return res.json({ success: true, message: "Resume deleted successfully" });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };





// src/controllers/resumeController.js

const path = require("path");
const fs = require("fs");
const Resume = require("../models/Resume");
const User = require("../models/user");
const pythonService = require("../services/pythonService");

/**
 * Upload & Process Resume (Production Ready)
 */
exports.uploadResume = async (req, res) => {
  try {
    if (!req.file)
      return res.status(400).json({ success: false, message: "No file uploaded" });

    const filePath = req.file.path;
    const filename = req.file.filename;
    const targetRole = req.body.targetRole || "fullstack-developer";

    console.log("📤 Sending file to Python service...");

    // ---- CALL PYTHON ----
    const result = await pythonService.processResume(filePath, targetRole);

    if (!result.success) {
      return res.status(400).json({
        success: false,
        message: "Python microservice failed",
      });
    }

    // ---------------------------------------------------------
    // ✅ ROBUST DATA EXTRACTION
    // ---------------------------------------------------------
    const rootData = result.parsedResume || result;
    const parsedObj = rootData.parsed || rootData || {};
    const analysisObj = rootData.analysis || {};

    // 1. Extract Score
    const score = analysisObj.resume_score || parsedObj.score || result.score || 0;

    // 2. Extract Feedback (Robust Fallback)
    let feedback = [];
    if (analysisObj.feedback && analysisObj.feedback.length > 0) feedback = analysisObj.feedback;
    else if (parsedObj.feedback && parsedObj.feedback.length > 0) feedback = parsedObj.feedback;

    // 3. Extract Strengths & Weaknesses (New Python Feature)
    // If Python didn't return them, we split the feedback list manually as a fallback
    let strengths = analysisObj.strengths || [];
    let weaknesses = analysisObj.weaknesses || [];

    if (strengths.length === 0 && feedback.length > 0) {
        // Fallback: First half of feedback is usually positive/general
        strengths = feedback.slice(0, Math.ceil(feedback.length / 2));
    }
    if (weaknesses.length === 0 && feedback.length > 0) {
        // Fallback: Second half often contains improvements
        weaknesses = feedback.slice(Math.ceil(feedback.length / 2));
    }

    // 4. Extract Standard Fields
    const skills = parsedObj.skills || [];
    const education = parsedObj.education || [];
    const experience = parsedObj.experience || [];

    // Safety: Ensure skills array isn't empty for Roadmap generation
    if (skills.length === 0) skills.push("General Technical Skills");

    console.log("📊 Parsed Data Summary:", {
      score,
      feedbackItems: feedback.length,
      strengths: strengths.length,
      skillsFound: skills.length
    });

    // ---------------------------------------------------------
    // ✅ REAL WORLD: CLEANUP OLD DATA
    // ---------------------------------------------------------
    // Find if user already has a resume
    const existingResume = await Resume.findOne({ userId: req.user._id });
    
    if (existingResume) {
        console.log("♻️ Deleting old resume for user...");
        // 1. Remove file from disk
        if (existingResume.fileURL) {
            const oldFilePath = path.join(__dirname, "..", "uploads", "resumes", path.basename(existingResume.fileURL));
            if (fs.existsSync(oldFilePath)) {
                try {
                    fs.unlinkSync(oldFilePath);
                } catch (e) {
                    console.warn("⚠️ Failed to delete old file:", e.message);
                }
            }
        }
        // 2. Remove record from DB
        await Resume.deleteOne({ _id: existingResume._id });
    }

    // ---------------------------------------------------------
    // ✅ SAVE NEW RESUME
    // ---------------------------------------------------------
    const resumeDoc = await Resume.create({
      userId: req.user._id,
      rawText: parsedObj.raw_text || "",
      skills: skills,
      education: education,
      experience: experience,
      score: score,
      feedback: feedback,
      strengths: strengths,   // Saved for UI
      weaknesses: weaknesses, // Saved for UI
      fileURL: `/uploads/resumes/${filename}`,
    });

    // ---- UPDATE USER MODEL ----
    await User.findByIdAndUpdate(req.user._id, {
      resumeUploaded: true,
      resumeScore: score,
      extractedSkills: skills,
      skillGaps: parsedObj.skill_gaps || [],
      roadmapGenerated: true,
      // We don't overwrite roadmap here to let the Roadmap page generate a fresh one dynamically
    });

    // ---- RETURN COMPLETE DATA TO FRONTEND ----
    return res.json({
      success: true,
      data: {
        resume: resumeDoc,
        parsedResume: {
          skills,
          education,
          experience,
          score,
          feedback,
          strengths,   // Frontend needs this
          weaknesses,  // Frontend needs this (often mapped to 'improvements')
          raw_text: parsedObj.raw_text || ""
        },
        roadmap: result.generatedRoadmap,
        pdf_url: `/uploads/resumes/${filename}`,
      },
    });

  } catch (err) {
    console.error("Upload Resume Error:", err.message);
    return res.status(500).json({
      success: false,
      message: "Server error",
      details: err.message,
    });
  }
};

// ... (Keep listUserResumes, getResume, deleteResume unchanged) ...
exports.listUserResumes = async (req, res) => {
  try {
    const resumes = await Resume.find({ userId: req.user._id }).sort({ createdAt: -1 });
    return res.json({ success: true, data: resumes });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

exports.getResume = async (req, res) => {
  try {
    const resume = await Resume.findById(req.params.id);
    if (!resume)
      return res.status(404).json({ success: false, message: "Resume not found" });
    return res.json({ success: true, data: resume });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

exports.deleteResume = async (req, res) => {
  try {
    const resume = await Resume.findById(req.params.id);
    if (!resume) return res.status(404).json({ success: false, message: "Resume not found" });

    if (resume.userId.toString() !== req.user._id.toString()) {
      return res.status(403).json({ success: false, message: "Not authorized" });
    }

    if (resume.fileURL) {
      const filePath = path.join(__dirname, "..", "uploads", "resumes", path.basename(resume.fileURL));
      try {
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
      } catch (e) {
        console.warn("File delete error:", e);
      }
    }

    await resume.deleteOne();
    return res.json({ success: true, message: "Resume deleted successfully" });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};