



// //For production
// const Resume = require("../models/Resume");
// const User = require("../models/user");
// const pythonService = require("../services/pythonService");

// /**
//  * UPLOAD & PROCESS RESUME (Production Ready)
//  * Handles Cloudinary URLs, Parsing, Gap Analysis, Roadmap, and DB Updates
//  */
// exports.uploadResume = async (req, res) => {
//   try {
//     // 1. Validation
//     if (!req.file) {
//       return res.status(400).json({ success: false, message: "No file uploaded" });
//     }

//     // 2. Get Cloudinary Details
//     const fileUrl = req.file.path; 
//     const publicId = req.file.filename; 
//     const targetRole = req.body.targetRole || "fullstack-developer";

//     console.log(`📤 Processing Resume URL: ${fileUrl} for role: ${targetRole}`);

//     // 3. Call Python Service (Parsing)
//     const result = await pythonService.processResume(fileUrl, targetRole);

//     if (!result || !result.success) {
//       return res.status(400).json({
//         success: false,
//         message: "Resume analysis failed by AI service",
//         error: result?.error || "Unknown error"
//       });
//     }

//     // ---------------------------------------------------------
//     // DATA EXTRACTION
//     // ---------------------------------------------------------
//     const rootData = result.parsedResume || result;
//     const parsedObj = rootData.parsed || rootData || {};
//     const analysisObj = rootData.analysis || {};

//     // Extract Score
//     const score = analysisObj.resume_score || parsedObj.score || result.score || 0;

//     // Extract Feedback
//     let feedback = analysisObj.feedback || parsedObj.feedback || [];
//     let strengths = analysisObj.strengths || [];
//     let weaknesses = analysisObj.weaknesses || [];

//     // Fallback: Manually split feedback if AI didn't categorize
//     if (strengths.length === 0 && feedback.length > 0) {
//         strengths = feedback.slice(0, Math.ceil(feedback.length / 2));
//     }
//     if (weaknesses.length === 0 && feedback.length > 0) {
//         weaknesses = feedback.slice(Math.ceil(feedback.length / 2));
//     }

//     // Extract Core Data
//     const skills = parsedObj.skills || ["General Technical Skills"];
//     const education = parsedObj.education || [];
//     const experience = parsedObj.experience || [];

//     // ---------------------------------------------------------
//     // NEW: AUTO-GENERATE GAPS & ROADMAP
//     // ---------------------------------------------------------
    
//     // 4. Generate Skill Gaps
//     let skillGaps = [];
//     try {
//         console.log("🔍 Analyzing Skill Gaps...");
//         const gapAnalysis = await pythonService.skillGapAnalyzer(skills, targetRole);
//         if (gapAnalysis && gapAnalysis.missing_skills) {
//             skillGaps = gapAnalysis.missing_skills;
//         }
//     } catch (gapErr) {
//         console.error("⚠️ Gap Analysis Failed (Non-fatal):", gapErr.message);
//     }

//     // 5. Generate Roadmap
//     let roadmap = [];
//     try {
//         console.log("🗺️ Generating Learning Roadmap...");
//         // Pass the skills (or gaps) to generate a roadmap
//         const roadmapData = await pythonService.generateRoadmap(skills, targetRole);
//         if (roadmapData && roadmapData.roadmap) {
//             roadmap = roadmapData.roadmap;
//         }
//     } catch (mapErr) {
//         console.error("⚠️ Roadmap Generation Failed (Non-fatal):", mapErr.message);
//     }

//     // ---------------------------------------------------------
//     // DATABASE UPDATES
//     // ---------------------------------------------------------

//     // 6. Cleanup Old Resume (DB Only)
//     await Resume.deleteMany({ userId: req.user._id });

//     // 7. Save New Resume to MongoDB
//     // Note: We add 'gaps' and 'roadmap' here if your Schema supports it.
//     // If your Resume schema doesn't have these fields, Mongoose will just ignore them (no crash).
//     const resumeDoc = await Resume.create({
//       userId: req.user._id,
//       rawText: parsedObj.raw_text || "",
//       skills: skills,
//       education: education,
//       experience: experience,
//       score: score,
//       feedback: feedback,
//       strengths: strengths,
//       weaknesses: weaknesses,
//       fileURL: fileUrl,       
//       fileId: publicId,
//       gaps: skillGaps,        // <--- Saving Gaps
//       roadmap: roadmap        // <--- Saving Roadmap
//     });

//     // 8. Update User Profile with the new AI insights
//     await User.findByIdAndUpdate(req.user._id, {
//       resumeUploaded: true,
//       resumeScore: score,
//       extractedSkills: skills,
//       skillGaps: skillGaps,   // <--- IMPORTANT for Dashboard
//       learningRoadmap: roadmap, // <--- IMPORTANT for Dashboard
//       roadmapGenerated: true,
//     });

//     console.log("✅ Resume Processing Complete.");

//     // 9. Return Success Response
//     return res.json({
//       success: true,
//       data: {
//         resume: resumeDoc,
//         parsedResume: {
//           skills, education, experience, score, feedback, strengths, weaknesses,
//           raw_text: parsedObj.raw_text || ""
//         },
//         gaps: skillGaps,     // Send back to frontend immediately
//         roadmap: roadmap,    // Send back to frontend immediately
//         pdf_url: fileUrl,
//       },
//     });

//   } catch (err) {
//     console.error("Upload Resume Error:", err);
//     return res.status(500).json({
//       success: false,
//       message: "Server error during resume processing",
//       details: err.message,
//     });
//   }
// };

// /**
//  * LIST USER RESUMES
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
//  * GET SPECIFIC RESUME
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
//  * DELETE RESUME
//  */
// exports.deleteResume = async (req, res) => {
//   try {
//     const resume = await Resume.findById(req.params.id);
//     if (!resume) return res.status(404).json({ success: false, message: "Resume not found" });

//     if (resume.userId.toString() !== req.user._id.toString()) {
//       return res.status(403).json({ success: false, message: "Not authorized" });
//     }

//     await resume.deleteOne();
//     return res.json({ success: true, message: "Resume deleted successfully" });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };





const Resume = require("../models/Resume");
const User = require("../models/user");
const pythonService = require("../services/pythonService");

// =========================================================
// 🧹 SANITIZATION HELPERS (The Fix for your Crash)
// =========================================================

// 1. Safe JSON Parser (Handles if AI returns a string instead of JSON)
const safeParse = (data) => {
    if (typeof data === 'string') {
        try {
            // Remove markdown code blocks if present (e.g., ```json ... ```)
            const cleanStr = data.replace(/```json/g, '').replace(/```/g, '').trim();
            return JSON.parse(cleanStr);
        } catch (e) {
            console.error("⚠️ Failed to parse stringified AI output:", e.message);
            return [];
        }
    }
    return data;
};

// 2. Flatten Gaps: { skill: "SQL", importance: 90 } -> "SQL"
const sanitizeGaps = (gapsRaw) => {
    const parsed = safeParse(gapsRaw);
    if (!Array.isArray(parsed)) return [];

    return parsed.map(item => {
        if (typeof item === 'string') return item;
        if (typeof item === 'object' && item.skill) return item.skill; // Extract skill name
        return "Unknown Skill";
    }).filter(Boolean); // Remove nulls
};

// 3. Flatten Roadmap: Handles Resources objects & Missing 'skill'
const sanitizeRoadmap = (roadmapRaw) => {
    const parsed = safeParse(roadmapRaw);
    if (!Array.isArray(parsed)) return [];

    return parsed.map((item, index) => {
        // Ensure 'skill' exists (Required by Schema)
        const skillName = item.skill || item.topic || item.area || `Skill Area ${index + 1}`;

        // Flatten Resources: { title: "X", type: "book" } -> "X (book)"
        let cleanResources = [];
        if (Array.isArray(item.resources)) {
            cleanResources = item.resources.map(res => {
                if (typeof res === 'string') return res;
                if (typeof res === 'object') {
                    // Combine title and type into a single string
                    return res.title ? `${res.title} (${res.type || 'Resource'})` : JSON.stringify(res);
                }
                return null;
            }).filter(Boolean);
        }

        return {
            skill: skillName,
            description: item.description || "Recommended learning path.",
            resources: cleanResources,
            status: "pending",
            deadline: item.deadline || null
        };
    });
};


// =========================================================
// 🚀 CONTROLLER METHODS
// =========================================================

exports.uploadResume = async (req, res) => {
  try {
    // 1. Validation
    if (!req.file) {
      return res.status(400).json({ success: false, message: "No file uploaded" });
    }

    // 2. Cloudinary Info
    const fileUrl = req.file.path; 
    const publicId = req.file.filename; 
    const targetRole = req.body.targetRole || "fullstack-developer";

    console.log(`📤 Processing Resume: ${fileUrl}`);

    // 3. AI Processing
    const result = await pythonService.processResume(fileUrl, targetRole);

    if (!result || !result.success) {
      return res.status(400).json({
        success: false, 
        message: "AI Analysis Failed", 
        error: result?.error 
      });
    }

    // 4. Data Extraction
    const rootData = result.parsedResume || result;
    const parsedObj = rootData.parsed || rootData || {};
    const analysisObj = rootData.analysis || {};

    // Score Cleaning
    let rawScore = analysisObj.resume_score || parsedObj.score || result.score || 0;
    let cleanScore = typeof rawScore === 'string' 
        ? parseInt(rawScore.replace(/\D/g, '')) || 0 
        : rawScore;
    if (cleanScore > 100) cleanScore = 100;

    // Feedback/Strengths/Weaknesses
    let feedback = analysisObj.feedback || parsedObj.feedback || [];
    let strengths = analysisObj.strengths || [];
    let weaknesses = analysisObj.weaknesses || [];

    // Fallback if AI puts everything in feedback
    if (strengths.length === 0 && feedback.length > 0) {
        strengths = feedback.slice(0, Math.ceil(feedback.length / 2));
    }

    const skills = parsedObj.skills || ["General Skills"];
    const education = parsedObj.education || [];
    const experience = parsedObj.experience || [];

    // ---------------------------------------------------------
    // 🧹 APPLYING THE FIX: SANITIZE GAPS & ROADMAP
    // ---------------------------------------------------------
    
    // 1. Get raw data from AI
    let rawGaps = [];
    try {
        const gapData = await pythonService.skillGapAnalyzer(skills, targetRole);
        rawGaps = gapData?.missing_skills || [];
    } catch (e) { console.error("Gap Analysis Error:", e.message); }

    let rawRoadmap = [];
    try {
        const roadData = await pythonService.generateRoadmap(skills, targetRole);
        rawRoadmap = roadData?.roadmap || [];
    } catch (e) { console.error("Roadmap Error:", e.message); }

    // 2. Clean Data using Helpers
    const cleanGaps = sanitizeGaps(rawGaps);
    const cleanRoadmap = sanitizeRoadmap(rawRoadmap);

    // ---------------------------------------------------------
    // DATABASE SAVING
    // ---------------------------------------------------------

    // Clear old resume
    await Resume.deleteMany({ userId: req.user._id });

    // Create new
    const resumeDoc = await Resume.create({
      userId: req.user._id,
      rawText: parsedObj.raw_text || "Parsed Content",
      skills: Array.isArray(skills) ? skills : [],
      education,
      experience,
      score: cleanScore,
      feedback: Array.isArray(feedback) ? feedback : [],
      strengths: Array.isArray(strengths) ? strengths : [],
      weaknesses: Array.isArray(weaknesses) ? weaknesses : [],
      fileURL: fileUrl,
      fileId: publicId,
      
      // ✅ Now using the Sanitized Data
      gaps: cleanGaps,
      roadmap: cleanRoadmap
    });

    // Update User Profile
    await User.findByIdAndUpdate(req.user._id, {
      resumeUploaded: true,
      resumeScore: cleanScore,
      extractedSkills: skills,
      skillGaps: cleanGaps,
      learningRoadmap: cleanRoadmap,
      roadmapGenerated: true,
    });

    console.log("✅ Resume Saved Successfully! Score:", cleanScore);

    return res.json({
      success: true,
      data: {
        resume: resumeDoc,
        gaps: cleanGaps,
        roadmap: cleanRoadmap
      }
    });

  } catch (err) {
    console.error("❌ Critical Upload Error:", err);
    
    // Detailed Validation Error Logging
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            success: false,
            message: "Data Validation Failed",
            details: Object.values(err.errors).map(e => e.message)
        });
    }

    return res.status(500).json({ success: false, message: "Server Error", error: err.message });
  }
};

// =========================================================
// CRUD METHODS (Restored)
// =========================================================

exports.listUserResumes = async (req, res) => {
  try {
    const resumes = await Resume.find({ userId: req.user._id }).sort({ createdAt: -1 });
    res.json({ success: true, data: resumes });
  } catch (err) { res.status(500).json({ success: false, message: "Error listing resumes" }); }
};

exports.getResume = async (req, res) => {
  try {
    const resume = await Resume.findById(req.params.id);
    if (!resume) return res.status(404).json({ success: false, message: "Not Found" });
    res.json({ success: true, data: resume });
  } catch (err) { res.status(500).json({ success: false, message: "Error retrieving resume" }); }
};

exports.deleteResume = async (req, res) => {
  try {
    await Resume.findOneAndDelete({ _id: req.params.id, userId: req.user._id });
    res.json({ success: true, message: "Deleted" });
  } catch (err) { res.status(500).json({ success: false, message: "Error deleting" }); }
};