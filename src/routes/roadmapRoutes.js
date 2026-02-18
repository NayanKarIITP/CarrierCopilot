

const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");
const {
  generateRoadmap,
  getUserRoadmaps,
  updateRoadmap,
  deleteRoadmap,
} = require("../controllers/roadmapController");

router.post("/generate", auth, generateRoadmap);

router.get("/", auth, getUserRoadmaps);


router.put("/:id", auth, updateRoadmap);

router.delete("/:id", auth, deleteRoadmap);

module.exports = router;