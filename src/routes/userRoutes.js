const express = require("express");
const router = express.Router();
const auth = require("../middleware/authMiddleware"); // Ensure you have this middleware
const { getProfile, updateProfile, changePassword } = require("../controllers/userController");

router.get("/profile", auth, getProfile);
router.put("/profile", auth, updateProfile);   // Matches "Save Profile"
router.put("/password", auth, changePassword); // Matches "Change Password"

module.exports = router;