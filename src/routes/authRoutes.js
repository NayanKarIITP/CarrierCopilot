
const express = require("express");
const router = express.Router();

const {
  registerUser,
  loginUser,
  googleAuth,
  getUserProfile
} = require("../controllers/authController");

const authMiddleware = require("../middleware/authMiddleware");

// Public routes
router.post("/signup", registerUser); 
router.post("/login", loginUser);
router.post("/google", googleAuth);  

// Protected route
router.get("/me", authMiddleware, getUserProfile);

module.exports = router;