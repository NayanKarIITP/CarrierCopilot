// const express = require("express");
// const router = express.Router();
// const auth = require("../middleware/authMiddleware");
// const {
//   generateRoadmap,
//   getUserRoadmaps,
//   updateRoadmap,
//   deleteRoadmap,
// } = require("../controllers/roadmapController");

// // Generate AI roadmap
// router.post("/generate", auth, generateRoadmap);

// // Get all user roadmaps
// router.get("/", auth, getUserRoadmaps);

// // Update a roadmap
// router.put("/:id", auth, updateRoadmap);

// // Delete roadmap
// router.delete("/:id", auth, deleteRoadmap);

// module.exports = router;






// const express = require("express");
// const router = express.Router();
// const auth = require("../middleware/authMiddleware");
// const {
//   generateRoadmap,
//   getUserRoadmaps,
//   updateRoadmap,
//   deleteRoadmap,
// } = require("../controllers/roadmapController");

// // Generate AI roadmap (POST /api/roadmap/generate)
// router.post("/generate", auth, generateRoadmap);

// // Get all user roadmaps (GET /api/roadmap)
// router.get("/", auth, getUserRoadmaps);

// // Update a roadmap (PUT /api/roadmap/:id)
// router.put("/:id", auth, updateRoadmap);

// // Delete roadmap (DELETE /api/roadmap/:id)
// router.delete("/:id", auth, deleteRoadmap);

// module.exports = router;









//roadmapRoutes.js
const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");
const {
  generateRoadmap,
  getUserRoadmaps,
  updateRoadmap,
  deleteRoadmap,
} = require("../controllers/roadmapController");

// @route   POST /api/roadmap/generate
// @desc    Generate AI roadmap
// @access  Private (Required to access User History/Skills from DB)
router.post("/generate", auth, generateRoadmap);

// @route   GET /api/roadmap
// @desc    Get all past roadmaps for the logged-in user
// @access  Private
router.get("/", auth, getUserRoadmaps);

// @route   PUT /api/roadmap/:id
// @desc    Update a roadmap (e.g., mark steps as complete or change role)
// @access  Private
router.put("/:id", auth, updateRoadmap);

// @route   DELETE /api/roadmap/:id
// @desc    Delete a roadmap
// @access  Private
router.delete("/:id", auth, deleteRoadmap);

module.exports = router;