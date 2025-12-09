
// // src/controllers/dashboardController.js

// const User = require("../models/user");
// const Resume = require("../models/Resume");
// const Roadmap = require("../models/Roadmap");
// const Trends = require("../models/Trends");
// const pythonService = require("../services/pythonService");

// exports.getDashboard = async (req, res) => {
//   try {
//     const userId = req.user._id;

//     // Fetch user
//     const user = await User.findById(userId).select("-password");

//     if (!user) {
//       return res.status(404).json({ success: false, message: "User not found" });
//     }

//     // Fetch latest resume
//     const latestResume = await Resume.findOne({ userId }).sort({ createdAt: -1 });

//     let parsedResume = null;
//     let skillGap = null;
//     let roadmap = null;

//     //--------------------------------------------
//     // 🔥 1. If user uploaded a resume → Analyze it
//     //--------------------------------------------
//     if (latestResume && latestResume.textContent) {
//       parsedResume = await pythonService.analyzeResume(latestResume.textContent);

//       // Example Python return:
//       // {
//       //   score: 82,
//       //   grade: "B+",
//       //   skills: ["React", "Node", "ML"],
//       //   recommendations: ["Learn Redux", "Improve SQL"]
//       // }

//       // Update user fields in MongoDB
//       user.resumeScore = parsedResume.score;
//       user.resumeGrade = parsedResume.grade;
//       user.extractedSkills = parsedResume.skills;
//       user.resumeUploaded = true;

//       await user.save();

//       //--------------------------------------------
//       // 🔥 2. Skill Gap Analysis (Python)
//       //--------------------------------------------
//       skillGap = await pythonService.skillGapAnalyzer(
//         parsedResume.skills,
//         user.targetRole || "Software Engineer"
//       );

//       user.skillGaps = skillGap.gaps;
//       await user.save();

//       //--------------------------------------------
//       // 🔥 3. Learning Roadmap (Python)
//       //--------------------------------------------
//       roadmap = await pythonService.generateRoadmap(
//         parsedResume.skills,
//         user.targetRole || "Software Engineer"
//       );

//       // Store roadmap in DB
//       await Roadmap.findOneAndUpdate(
//         { userId },
//         { steps: roadmap.steps, progress: roadmap.progress },
//         { upsert: true }
//       );
//     }

//     //--------------------------------------------
//     // Fetch roadmap and trends
//     //--------------------------------------------
//     const roadmapDoc = await Roadmap.findOne({ userId }).sort({ createdAt: -1 });
//     const trends = await Trends.findOne().sort({ createdAt: -1 });

//     //--------------------------------------------
//     // FINAL RESPONSE
//     //--------------------------------------------
//     return res.json({
//       success: true,
//       data: {
//         user: {
//           fullName: user.fullName,
//           photoURL: user.photoURL,
//           lastLogin: user.lastLogin,
//         },

//         resume: {
//           uploaded: user.resumeUploaded,
//           score: user.resumeScore,
//           grade: user.resumeGrade,
//           skills: user.extractedSkills,
//           gaps: user.skillGaps,
//           latest: latestResume,
//         },

//         roadmap: {
//           generated: user.roadmapGenerated,
//           roadmap: roadmapDoc,
//         },

//         trends: trends || null,

//         aiTips: parsedResume?.recommendations || [],

//         stats: {
//           totalUploads: await Resume.countDocuments({ userId }),
//           totalInterviews: 0, // you can replace this later
//         }
//       }
//     });

//   } catch (err) {
//     console.error("Dashboard Error:", err);
//     return res.status(500).json({ success: false, message: "Dashboard fetch error" });
//   }
// };






// const User = require("../models/user");
// const Resume = require("../models/Resume");
// const Roadmap = require("../models/Roadmap");
// const Trends = require("../models/Trends");

// const pythonService = require("../services/pythonService"); // Key

// // Role → Required Skills Mapping
// const ROLE_SKILLS = {
//   "fullstack-developer": [
//     "React", "Node.js", "MongoDB", "Express", "Docker",
//     "CI/CD", "Linux", "API Design", "System Design",
//     "Redis", "SQL", "NoSQL"
//   ],
//   "data-scientist": [
//     "Python", "Pandas", "Numpy", "TensorFlow", "PyTorch",
//     "Statistics", "Machine Learning", "Deep Learning",
//     "SQL", "Data Visualization"
//   ],
// };

// exports.getDashboard = async (req, res) => {
//   try {
//     const userId = req.user._id;

//     // Fetch user
//     const user = await User.findById(userId).select("-password");

//     // Fetch last uploaded resume
//     const latestResume = await Resume.findOne({ userId }).sort({ createdAt: -1 });

//     // Default return if no resume found
//     if (!latestResume) {
//       return res.json({
//         success: true,
//         data: {
//           user: {
//             fullName: user.fullName,
//             targetRole: user.targetRole || null,
//           },
//           resume: {
//             uploaded: false,
//             score: 0,
//             skills: [],
//             feedback: [],
//             gaps: [],
//           },
//           roadmap: {
//             generated: false,
//             roadmap: [],
//           },
//           aiTips: [],
//           trends: null,
//           stats: {
//             totalUploads: 0,
//             totalInterviews: 0,
//           }
//         }
//       });
//     }

//     // ----------------------------------------------------------------
//     // STEP 1 — Get Resume Skills
//     // ----------------------------------------------------------------
//     const resumeSkills = latestResume.skills || [];
//     const targetRole = user.targetRole || "fullstack-developer";
//     const targetRoleSkills = ROLE_SKILLS[targetRole] || [];

//     // ----------------------------------------------------------------
//     // STEP 2 — Skill Gap Analysis via Python Microservice
//     // ----------------------------------------------------------------
//     const gapResponse = await pythonService.skillGapAnalyzer(resumeSkills, targetRoleSkills);


//     const skillGaps = gapResponse?.skillGap || [];


//     // ----------------------------------------------------------------
//     // STEP 3 — Dynamic Roadmap Generation
//     // ----------------------------------------------------------------
//     const roadmapResponse = await pythonService.generateRoadmap(
//       resumeSkills,
//       targetRole
//     );

//     const roadmapSteps = roadmapResponse?.roadmap?.steps || [];

//     // ----------------------------------------------------------------
//     // STEP 4 — Fetch Market Trends
//     // ----------------------------------------------------------------
//     const latestTrends = await Trends.findOne().sort({ createdAt: -1 });

//     // ----------------------------------------------------------------
//     // STEP 5 — Stats
//     // ----------------------------------------------------------------
//     const stats = {
//       totalUploads: await Resume.countDocuments({ userId }),
//       totalInterviews: 0,
//     };

//     // ----------------------------------------------------------------
//     // FINAL RESPONSE
//     // EXACT MATCH with frontend usage
//     // ----------------------------------------------------------------
//     return res.json({
//       success: true,
//       data: {
//         user: {
//           fullName: user.fullName,
//           targetRole,
//         },

//         resume: {
//           uploaded: true,
//           score: latestResume.score,
//           skills: resumeSkills,
//           feedback: latestResume.feedback || [],
//           gaps: skillGaps,
//           education: latestResume.education || [],
//           experience: latestResume.experience || [],
//           fileURL: latestResume.fileURL,
//         },

//         roadmap: {
//           generated: roadmapSteps.length > 0,
//           roadmap: roadmapSteps,
//         },

//         aiTips: latestResume.feedback || [],

//         trends: latestTrends || null,

//         stats,
//       },
//     });

//   } catch (err) {
//     console.error("Dashboard Error:", err);
//     res.status(500).json({
//       success: false,
//       message: "Dashboard fetch error",
//     });
//   }
// };






const User = require("../models/user");
const Resume = require("../models/Resume");
// ✅ Ensure these models exist in your src/models folder!
const Roadmap = require("../models/Roadmap");
const Trends = require("../models/Trends"); 

const pythonService = require("../services/pythonService");

// Role → Required Skills Mapping
const ROLE_SKILLS = {
  "fullstack-developer": [
    "React", "Node.js", "MongoDB", "Express", "Docker",
    "CI/CD", "Linux", "API Design", "System Design",
    "Redis", "SQL", "NoSQL"
  ],
  "data-scientist": [
    "Python", "Pandas", "Numpy", "TensorFlow", "PyTorch",
    "Statistics", "Machine Learning", "Deep Learning",
    "SQL", "Data Visualization"
  ],
};

exports.getDashboard = async (req, res) => {
  try {
    const userId = req.user._id;

    // 🟦 DEBUG LOG 1: Which user is requesting dashboard
    console.log("\n===============================");
    console.log("🟦 DASHBOARD USER ID:", userId);

    // Fetch user
    const user = await User.findById(userId).select("-password");

    if (!user) {
      return res.status(404).json({ success: false, message: "User not found" });
    }

    // Fetch last uploaded resume
    const latestResume = await Resume.findOne({ userId }).sort({ createdAt: -1 });

    // ✅ Initialize default values if no resume found
    let resumeData = {
      uploaded: false,
      score: 0,
      skills: [],
      feedback: [],
      gaps: [],
      education: [],
      experience: [],
      fileURL: null
    };

    let roadmapData = {
      generated: false,
      roadmap: []
    };

    let aiTipsData = [];
    let skillGaps = [];

    // ✅ If resume exists, populate data
    if (latestResume) {
      resumeData = {
        uploaded: true,
        score: latestResume.score || 0,
        skills: latestResume.skills || [],
        feedback: latestResume.feedback || [],
        gaps: [], // Will be filled by skill gap analysis
        education: latestResume.education || [],
        experience: latestResume.experience || [],
        fileURL: latestResume.fileURL,
      };

      // AI Tips are just the feedback
      aiTipsData = latestResume.feedback || [];

      // --- ON-THE-FLY SKILL GAP ANALYSIS (Optional) ---
      // If you want to recalculate gaps every time dashboard loads:
      const targetRole = user.targetRole || "fullstack-developer";
      const targetRoleSkills = ROLE_SKILLS[targetRole] || [];
      
      // Check if skill gaps are already saved on User (preferred), otherwise calculate
      if (user.skillGaps && user.skillGaps.length > 0) {
          skillGaps = user.skillGaps;
      } else {
          // You could call pythonService here if needed, but usually 
          // this is done during upload. For now, let's use what's on User or empty.
          skillGaps = []; 
      }
      resumeData.gaps = skillGaps;

      // --- ROADMAP ---
      // Check if roadmap is saved on User
      if (user.roadmap && user.roadmap.steps && user.roadmap.steps.length > 0) {
          roadmapData = {
              generated: true,
              roadmap: user.roadmap.steps
          };
      }
    }

    // Fetch Trends (Optional - handle if model missing)
    let latestTrends = null;
    try {
        latestTrends = await Trends.findOne().sort({ createdAt: -1 });
    } catch (error) {
        console.warn("⚠️ Could not fetch trends (Model might be missing).");
    }

    // Stats
    const stats = {
      totalUploads: await Resume.countDocuments({ userId }),
      totalInterviews: 0, // Placeholder
    };

    // ✅ Final Response Structure
    return res.json({
      success: true,
      data: {
        user: {
          fullName: user.fullName || user.username || "User",
          targetRole: user.targetRole || "fullstack-developer",
        },
        resume: resumeData,
        roadmap: roadmapData,
        aiTips: aiTipsData,
        trends: latestTrends || null,
        stats,
      },
    });

  } catch (err) {
    console.error("❌ Dashboard Error:", err);
    return res.status(500).json({
      success: false,
      message: "Dashboard fetch error",
    });
  }
};