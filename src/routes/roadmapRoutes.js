const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");
const {
  generateRoadmap,
  getUserRoadmaps,
  updateRoadmap,
  deleteRoadmap,
} = require("../controllers/roadmapController");

// Generate AI roadmap
router.post("/generate", auth, generateRoadmap);

// Get all user roadmaps
router.get("/", auth, getUserRoadmaps);

// Update a roadmap
router.put("/:id", auth, updateRoadmap);

// Delete roadmap
router.delete("/:id", auth, deleteRoadmap);

module.exports = router;
