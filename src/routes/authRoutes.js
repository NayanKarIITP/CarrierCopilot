// const express = require("express");
// const router = express.Router();
// const {
//   registerUser,
//   loginUser,
//   googleAuth,
//   getUserProfile,
// } = require("../controllers/authController");
// const authMiddleware = require("../middleware/authMiddleware");

// // USER REGISTRATION
// router.post("/register", registerUser);

// // USER LOGIN
// router.post("/login", loginUser);

// // GOOGLE LOGIN
// router.post("/google-auth", googleAuth);

// // USER PROFILE (PROTECTED)
// router.get("/me", authMiddleware, getUserProfile);

// module.exports = router;




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
router.post("/register", registerUser);
router.post("/login", loginUser);
router.post("/google", googleAuth);

// Protected route
router.get("/me", authMiddleware, getUserProfile);

module.exports = router;
