

// src/controllers/roadmapController.js

const Roadmap = require("../models/Roadmap");
const User = require("../models/user"); 
const pythonService = require("../services/pythonService");

// Generate AI Roadmap

async function generateRoadmap(req, res) {
  try {
    let { skills, role } = req.body;
    const userId = req.user ? req.user._id : null;

    // 1. Fetch History if skills are missing
    if ((!skills || !Array.isArray(skills) || skills.length === 0) && userId) {
      console.log(`[Roadmap] Fetching historical skills for user: ${userId}`);
      const currentUser = await User.findById(userId).select("skills"); 
      
      if (currentUser && currentUser.skills && currentUser.skills.length > 0) {
        skills = currentUser.skills;
      } else {
        skills = ["HTML", "CSS", "JavaScript"]; // Default fallback
      }
    }

    // 2. Validate Inputs
    if (!skills || !Array.isArray(skills)) {
      return res.status(400).json({ success: false, message: "No skills found." });
    }
    if (!role) {
      return res.status(400).json({ success: false, message: "Target role is required." });
    }

    console.log(`[Roadmap] Generating for Role: ${role} | Skills: ${skills.length}`);

    // 3. Call Python Microservice
    // Python returns: { level: "Intermediate", roadmap: [...] }
    const aiResult = await pythonService.generateRoadmap(skills, role);

    if (!aiResult) {
      throw new Error("AI Service failed to return data");
    }

    // Handle structure (whether Python returns object or just array)
    const stepsData = aiResult.roadmap || aiResult;
    const levelData = aiResult.level || "Beginner"; 

    let savedRoadmap = null;

    // 4. Save to DB (Persistent History)
    if (userId) {
      savedRoadmap = await Roadmap.create({
        userId: userId,
        targetRole: role,
        steps: stepsData,
        currentSkills: skills,
        level: levelData // Save the Level!
      });

      // Update User Profile
      await User.findByIdAndUpdate(userId, {
        $set: { 
          roadmapGenerated: true,
          currentRoadmapId: savedRoadmap._id 
        }
      });
    }

    // 5. Send Response
    return res.json({
      success: true,
      data: {
        roadmap: stepsData,
        level: levelData, // Send level to Frontend
        savedId: savedRoadmap ? savedRoadmap._id : null,
      },
    });

  } catch (err) {
    console.error("Roadmap Generation Error:", err);
    return res.status(500).json({
      success: false,
      message: "Server error while generating roadmap",
      details: err.message,
    });
  }
}

// Get Roadmaps of Logged In User

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

// Update Roadmap by ID

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

// Delete Roadmap

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

// EXPORTS
module.exports = {
  generateRoadmap,
  getUserRoadmaps,
  updateRoadmap,
  deleteRoadmap,
};
