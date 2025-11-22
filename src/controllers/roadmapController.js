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
    const { skills, role } = req.body;

    // Validate skills
    if (!skills || !Array.isArray(skills)) {
      return res.status(400).json({
        success: false,
        message: "skills must be a valid list"
      });
    }

    // Validate role
    if (!role || typeof role !== "string") {
      return res.status(400).json({
        success: false,
        message: "role must be a valid string"
      });
    }

    // Call Python microservice
    const roadmapResult = await pythonService.generateRoadmap(skills, role);

    let savedRoadmap = null;

    // Save to DB if user logged in
    if (req.user) {
      savedRoadmap = await Roadmap.create({
        userId: req.user._id,
        targetRole: role,
        steps: roadmapResult.roadmap || [],
      });

      await User.findByIdAndUpdate(req.user._id, {
        roadmapGenerated: true,
        roadmap: roadmapResult,
      });
    }

    return res.json({
      success: true,
      data: {
        roadmap: roadmapResult,
        saved: savedRoadmap,
      },
    });

  } catch (err) {
    console.error("Roadmap Generation Error:", err);
    return res.status(500).json({
      success: false,
      message: "Server error",
      details: err.message,
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

    return res.json({ success: true, message: "Roadmap deleted" });

  } catch (err) {
    console.error("Delete Roadmap Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
}

/**
 * -------------------------------------------------------
 * EXPORTS (CLEAN & CONSISTENT)
 * -------------------------------------------------------
 */
module.exports = {
  generateRoadmap,
  getUserRoadmaps,
  updateRoadmap,
  deleteRoadmap,
};
