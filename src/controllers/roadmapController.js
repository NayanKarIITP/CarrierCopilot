
// // src/controllers/roadmapController.js

// const Roadmap = require("../models/Roadmap");
// const User = require("../models/user"); // Ensure filename casing matches your system
// const pythonService = require("../services/pythonService");

// /**
//  * -------------------------------------------------------
//  * Generate AI Roadmap
//  * Real-world logic: Uses provided skills OR fetches 
//  * user's existing profile history from DB.
//  * -------------------------------------------------------
//  */
// async function generateRoadmap(req, res) {
//   try {
//     let { skills, role } = req.body;
//     const userId = req.user ? req.user._id : null;

//     // 1. "Take history from prev page/DB"
//     // If skills are missing in the request body, fetch them from the User's profile
//     if ((!skills || !Array.isArray(skills) || skills.length === 0) && userId) {
//       console.log(`[Roadmap] Fetching historical skills for user: ${userId}`);
      
//       const currentUser = await User.findById(userId).select("skills projects"); 
      
//       // Assuming 'skills' is an array of strings in your User model
//       if (currentUser && currentUser.skills && currentUser.skills.length > 0) {
//         skills = currentUser.skills;
//       } else {
//         // Fallback if user has no history in DB
//         skills = ["HTML", "CSS", "JavaScript"]; 
//       }
//     }

//     // 2. Validate Inputs
//     if (!skills || !Array.isArray(skills)) {
//       return res.status(400).json({
//         success: false,
//         message: "No skills found. Please update your profile or select skills manually."
//       });
//     }

//     if (!role || typeof role !== "string") {
//       return res.status(400).json({
//         success: false,
//         message: "Target role is required (e.g., 'Senior Full-Stack Developer')."
//       });
//     }

//     console.log(`[Roadmap] Generating for Role: ${role} | Skills: ${skills.length}`);

//     // 3. Call Python Microservice (AI Logic)
//     // This service should return the JSON structure required by your Frontend
//     const roadmapResult = await pythonService.generateRoadmap(skills, role);

//     if (!roadmapResult) {
//       throw new Error("AI Service failed to return data");
//     }

//     let savedRoadmap = null;

//     // 4. Save to DB (Persistent History)
//     if (userId) {
//       // Create new Roadmap entry
//       savedRoadmap = await Roadmap.create({
//         userId: userId,
//         targetRole: role,
//         steps: roadmapResult.roadmap || [], // Ensure this matches python response structure
//         currentSkills: skills // Save what skills were used to generate this
//       });

//       // Link to User Profile
//       await User.findByIdAndUpdate(userId, {
//         $set: { 
//           roadmapGenerated: true,
//           currentRoadmapId: savedRoadmap._id 
//         }
//       });
//     }

//     // 5. Send Response
//     return res.json({
//       success: true,
//       data: {
//         roadmap: roadmapResult.roadmap || roadmapResult, // Adapt based on Python return shape
//         savedId: savedRoadmap ? savedRoadmap._id : null,
//       },
//     });

//   } catch (err) {
//     console.error("Roadmap Generation Error:", err);
//     return res.status(500).json({
//       success: false,
//       message: "Server error while generating roadmap",
//       details: err.message,
//     });
//   }
// }

// /**
//  * -------------------------------------------------------
//  * Get Roadmaps of Logged In User
//  * -------------------------------------------------------
//  */
// async function getUserRoadmaps(req, res) {
//   try {
//     // Return latest roadmap first
//     const list = await Roadmap.find({ userId: req.user._id })
//       .sort({ createdAt: -1 });

//     return res.json({ success: true, data: list });

//   } catch (err) {
//     console.error("Get Roadmaps Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// }

// /**
//  * -------------------------------------------------------
//  * Update Roadmap by ID
//  * -------------------------------------------------------
//  */
// async function updateRoadmap(req, res) {
//   try {
//     const roadmap = await Roadmap.findById(req.params.id);

//     if (!roadmap) {
//       return res.status(404).json({ success: false, message: "Roadmap not found" });
//     }

//     if (roadmap.userId.toString() !== req.user._id.toString()) {
//       return res.status(403).json({ success: false, message: "Not authorized" });
//     }

//     // Allow updating specific fields
//     roadmap.steps = req.body.steps || roadmap.steps;
//     roadmap.targetRole = req.body.targetRole || roadmap.targetRole;
    
//     await roadmap.save();

//     return res.json({ success: true, data: roadmap });

//   } catch (err) {
//     console.error("Update Roadmap Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// }

// /**
//  * -------------------------------------------------------
//  * Delete Roadmap
//  * -------------------------------------------------------
//  */
// async function deleteRoadmap(req, res) {
//   try {
//     const roadmap = await Roadmap.findById(req.params.id);

//     if (!roadmap) {
//       return res.status(404).json({ success: false, message: "Roadmap not found" });
//     }

//     if (roadmap.userId.toString() !== req.user._id.toString()) {
//       return res.status(403).json({ success: false, message: "Not authorized" });
//     }

//     await roadmap.deleteOne();

//     return res.json({ success: true, message: "Roadmap deleted successfully" });

//   } catch (err) {
//     console.error("Delete Roadmap Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// }

// /**
//  * -------------------------------------------------------
//  * EXPORTS
//  * -------------------------------------------------------
//  */
// module.exports = {
//   generateRoadmap,
//   getUserRoadmaps,
//   updateRoadmap,
//   deleteRoadmap,
// };









// src/controllers/roadmapController.js

const Roadmap = require("../models/Roadmap");
const User = require("../models/user"); 
const pythonService = require("../services/pythonService");

/**
 * -------------------------------------------------------
 * Generate AI Roadmap
 * -------------------------------------------------------
 */
async function generateRoadmap(req, res) {
  try {
    let { skills, role } = req.body;
    const userId = req.user ? req.user._id : null;

    // 1. Fetch History if skills missing
    if ((!skills || !Array.isArray(skills) || skills.length === 0) && userId) {
      const currentUser = await User.findById(userId).select("skills");
      skills = currentUser?.skills?.length
        ? currentUser.skills
        : ["HTML", "CSS", "JavaScript"];
    }

    if (!skills || !Array.isArray(skills)) {
      return res.status(400).json({ success: false, message: "No skills found." });
    }
    if (!role) {
      return res.status(400).json({ success: false, message: "Target role is required." });
    }

    console.log(`[Roadmap] Generating for ${role}`);

    // 2. Call Python
    const aiResult = await pythonService.generateRoadmap(skills, role);

    // 🛡️ CRITICAL FIX: FALLBACK INSTEAD OF THROW
    let stepsData;
    let levelData = "Beginner";

    if (!aiResult) {
      console.warn("⚠️ Python roadmap failed, using fallback");

      stepsData = [
        { step: "Strengthen core fundamentals" },
        { step: "Build 2–3 real-world projects" },
        { step: "Learn DSA and problem solving" },
        { step: "Prepare interview questions" },
        { step: "Apply consistently" },
      ];
    } else {
      stepsData = aiResult.roadmap || aiResult;
      levelData = aiResult.level || "Intermediate";
    }

    let savedRoadmap = null;

    // 3. Save roadmap
    if (userId) {
      savedRoadmap = await Roadmap.create({
        userId,
        targetRole: role,
        steps: stepsData,
        currentSkills: skills,
        level: levelData,
      });

      await User.findByIdAndUpdate(userId, {
        roadmapGenerated: true,
        currentRoadmapId: savedRoadmap._id,
      });
    }

    return res.json({
      success: true,
      data: {
        roadmap: stepsData,
        level: levelData,
        savedId: savedRoadmap ? savedRoadmap._id : null,
        fallback: !aiResult, // 👈 frontend can show badge if needed
      },
    });

  } catch (err) {
    console.error("Roadmap Generation Error:", err.message);
    return res.status(500).json({
      success: false,
      message: "Roadmap generation failed",
    });
  }
}

/**
 * -------------------------------------------------------
 * Get Roadmaps of Logged In User
 * -------------------------------------------------------
 */
async function getUserRoadmaps(req, res) {
  try {
    // Return latest roadmap first
    const list = await Roadmap.find({ userId: req.user._id })
      .sort({ createdAt: -1 });

    return res.json({ success: true, data: list });

  } catch (err) {
    console.error("Get Roadmaps Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
}

/**
 * -------------------------------------------------------
 * Update Roadmap by ID
 * -------------------------------------------------------
 */
async function updateRoadmap(req, res) {
  try {
    const roadmap = await Roadmap.findById(req.params.id);

    if (!roadmap) {
      return res.status(404).json({ success: false, message: "Roadmap not found" });
    }

    if (roadmap.userId.toString() !== req.user._id.toString()) {
      return res.status(403).json({ success: false, message: "Not authorized" });
    }

    // Allow updating specific fields
    roadmap.steps = req.body.steps || roadmap.steps;
    roadmap.targetRole = req.body.targetRole || roadmap.targetRole;
    
    await roadmap.save();

    return res.json({ success: true, data: roadmap });

  } catch (err) {
    console.error("Update Roadmap Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
}

/**
 * -------------------------------------------------------
 * Delete Roadmap
 * -------------------------------------------------------
 */
async function deleteRoadmap(req, res) {
  try {
    const roadmap = await Roadmap.findById(req.params.id);

    if (!roadmap) {
      return res.status(404).json({ success: false, message: "Roadmap not found" });
    }

    if (roadmap.userId.toString() !== req.user._id.toString()) {
      return res.status(403).json({ success: false, message: "Not authorized" });
    }

    await roadmap.deleteOne();

    return res.json({ success: true, message: "Roadmap deleted successfully" });

  } catch (err) {
    console.error("Delete Roadmap Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
}

/**
 * -------------------------------------------------------
 * EXPORTS
 * -------------------------------------------------------
 */
module.exports = {
  generateRoadmap,
  getUserRoadmaps,
  updateRoadmap,
  deleteRoadmap,
};
