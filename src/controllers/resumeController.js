const Resume = require("../models/Resume");
const User = require("../models/user");
const pythonService = require("../services/pythonService");

//  SANITIZATION HELPERS

// 1. Safe JSON Parser
const safeParse = (data) => {
    if (typeof data === 'string') {
        try {
            const cleanStr = data.replace(/```json/g, '').replace(/```/g, '').trim();
            return JSON.parse(cleanStr);
        } catch (e) {
            console.error("⚠️ Failed to parse stringified AI output:", e.message);
            return [];
        }
    }
    return data;
};

// 2. Flatten Gaps
const sanitizeGaps = (gapsRaw) => {
    const parsed = safeParse(gapsRaw);
    if (!Array.isArray(parsed)) return [];

    return parsed.map(item => {
        if (typeof item === 'string') return item;
        if (typeof item === 'object' && item.skill) return item.skill;
        return "Unknown Skill";
    }).filter(Boolean);
};

// 3. Flatten Roadmap
const sanitizeRoadmap = (roadmapRaw) => {
    const parsed = safeParse(roadmapRaw);
    if (!Array.isArray(parsed)) return [];

    return parsed.map((item, index) => {
        const skillName = item.skill || item.topic || item.area || `Skill Area ${index + 1}`;
        
        let cleanResources = [];
        if (Array.isArray(item.resources)) {
            cleanResources = item.resources.map(res => {
                if (typeof res === 'string') return res;
                if (typeof res === 'object') {
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


//  CONTROLLER METHODS

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

    console.log(` Processing Resume: ${fileUrl}`);

    // 3. AI Processing (Resume Parsing)
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

    if (strengths.length === 0 && feedback.length > 0) {
        strengths = feedback.slice(0, Math.ceil(feedback.length / 2));
    }

    const skills = parsedObj.skills || ["General Skills"];
    const education = parsedObj.education || [];
    const experience = parsedObj.experience || [];

    //  PARALLEL AI EXECUTION (The Fix for Timeout)
    
    console.log(" Starting Parallel AI Tasks (Gaps & Roadmap)...");

    // We run both promises at once using Promise.all
    // We attach .catch() to each individually so one failure doesn't stop the whole upload
    const [gapData, roadData] = await Promise.all([
        pythonService.skillGapAnalyzer(skills, targetRole).catch(e => {
            console.error(" Gap Analysis Error:", e.message);
            return { missing_skills: [] };
        }),
        pythonService.generateRoadmap(skills, targetRole).catch(e => {
            console.error(" Roadmap Error:", e.message);
            return { roadmap: [] };
        })
    ]);

    console.log(" Parallel AI Tasks Complete.");

    const rawGaps = gapData?.missing_skills || [];
    const rawRoadmap = roadData?.roadmap || [];

    // 5. Clean Data using Helpers
    const cleanGaps = sanitizeGaps(rawGaps);
    const cleanRoadmap = sanitizeRoadmap(rawRoadmap);

    // DATABASE SAVING

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

    console.log(" Resume Saved Successfully! Score:", cleanScore);

    return res.json({
      success: true,
      data: {
        resume: resumeDoc,
        gaps: cleanGaps,
        roadmap: cleanRoadmap
      }
    });

  } catch (err) {
    console.error(" Critical Upload Error:", err);
    
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


// CRUD METHODS


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