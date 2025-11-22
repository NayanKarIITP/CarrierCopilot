const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware");

const {
  getSettings,
  updateSettings
} = require("../controllers/settingsController");

// Get settings
router.get("/", auth, getSettings);

// Update settings
router.put("/", auth, updateSettings);

module.exports = router;
