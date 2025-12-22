// const express = require("express");
// const router = express.Router();

// const upload = require("../middleware/uploadMiddleware");
// const auth = require("../middleware/authMiddleware");

// const {
//   uploadResume,
//   listUserResumes,
//   getResume,
//   deleteResume,
// } = require("../controllers/resumeController");

// const pythonService = require("../services/pythonService");

// // -------------------------------------
// // RESUME FILE CRUD ROUTES
// // -------------------------------------

// // Upload + Analyze Resume (PROTECTED)
// router.post("/upload", auth, upload.single("resume"), uploadResume);

// // Get all resumes (PROTECTED)
// router.get("/", auth, listUserResumes);

// // Get single resume (PROTECTED)
// router.get("/:id", auth, getResume);

// // Delete resume (PROTECTED)
// router.delete("/:id", auth, deleteResume);

// // -------------------------------------
// // AI MICRO-SERVICE ROUTES
// // -------------------------------------

// // 🔹 AI Resume Parsing From TEXT
// // POST /api/resume/parse-text
// router.post("/parse-text", auth, async (req, res) => {
//   try {
//     const { text, target_role } = req.body;

//     if (!text) {
//       return res.status(400).json({ message: "Text is required" });
//     }

//     const result = await pythonService.parseResumeText(text, target_role);
//     return res.json(result);

//   } catch (err) {
//     console.error("Parse-text error:", err);
//     return res.status(500).json({ message: "AI text parsing failed" });
//   }
// });

// // 🔹 AI Roadmap Generation
// router.post("/roadmap", auth, async (req, res) => {
//   try {
//     const { skills, role } = req.body;

//     if (!skills || !role) {
//       return res.status(400).json({ message: "skills and role required" });
//     }

//     const result = await pythonService.generateRoadmap(skills, role);
//     return res.json(result);

//   } catch (err) {
//     console.error("Roadmap error:", err);
//     return res.status(500).json({ message: "AI roadmap generation failed" });
//   }
// });

// // 🔹 AI Skill Gap Analyzer
// router.post("/skill-gap", auth, async (req, res) => {
//   try {
//     const { resumeSkills, targetRole } = req.body;

//     const result = await pythonService.skillGapAnalyzer(
//       resumeSkills,
//       targetRole
//     );

//     return res.json(result);

//   } catch (err) {
//     console.error("Skill gap error:", err);
//     return res.status(500).json({ message: "AI skill gap analysis failed" });
//   }
// });

// module.exports = router;






//Last working one
// const express = require("express");
// const router = express.Router();

// const upload = require("../middleware/uploadMiddleware");
// const auth = require("../middleware/authMiddleware");

// const {
//   uploadResume,
//   listUserResumes,
//   getResume,
//   deleteResume,
// } = require("../controllers/resumeController");

// const pythonService = require("../services/pythonService");

// // -------------------------------------------------------
// // 🔹 MAIN UPLOAD ROUTE
// // -------------------------------------------------------
// // Ensure your frontend sends form-data with key 'file'
// router.post("/upload", auth, upload.single("resume"), uploadResume);


// // -------------------------------------------------------
// // CRUD Routes
// // -------------------------------------------------------
// router.get("/", auth, listUserResumes);           // List all
// router.get("/:id", auth, getResume);              // Get specific
// router.delete("/:id", auth, deleteResume);        // Delete

// // -------------------------------------------------------
// // 🔹 AI Utility Routes (Direct Service Calls)
// // -------------------------------------------------------

// router.post("/parse-text", auth, async (req, res) => {
//   try {
//     const { text, target_role } = req.body;

//     const result = await pythonService.analyzeResume(text, target_role);

//     console.log("🐍 PYTHON RESULT ===>", result);

//     return res.json({
//       success: true,
//       data: result,
//     });

//   } catch (err) {
//     console.error("Parse-text error:", err);
//     return res.status(500).json({ message: "AI text parsing failed" });
//   }
// });


// // 2. Roadmap Generation
// router.post("/roadmap", auth, async (req, res) => {
//   try {
//     const { skills, role } = req.body;

//     if (!skills || !role) {
//       return res.status(400).json({ message: "skills and role required" });
//     }

//     const result = await pythonService.generateRoadmap(skills, role);
//     return res.json(result);

//   } catch (err) {
//     console.error("Roadmap error:", err);
//     return res.status(500).json({ message: "AI roadmap generation failed" });
//   }
// });

// // 3. Skill Gap Analyzer
// router.post("/skill-gap", auth, async (req, res) => {
//   try {
//     const { resumeSkills, targetRole } = req.body;

//     const result = await pythonService.skillGapAnalyzer(
//       resumeSkills,
//       targetRole
//     );

//     return res.json(result);

//   } catch (err) {
//     console.error("Skill gap error:", err);
//     return res.status(500).json({ message: "AI skill gap analysis failed" });
//   }
// });

// const path = require("path");
// const fs = require("fs");

// // -------------------------------------------------------
// // 🔹 SERVE UPLOADED RESUME PDF (PRODUCTION SAFE)
// // -------------------------------------------------------
// router.get("/file/:filename", auth, (req, res) => {
//   try {
//     const filePath = path.join(
//       __dirname,
//       "../../uploads",
//       req.params.filename
//     );

//     if (!fs.existsSync(filePath)) {
//       return res.status(404).json({
//         success: false,
//         message: "Resume file not found",
//       });
//     }

//     res.setHeader("Content-Type", "application/pdf");
//     res.sendFile(filePath);
//   } catch (err) {
//     console.error("Resume file serve error:", err);
//     res.status(500).json({ success: false });
//   }
// });

// module.exports = router;






const express = require("express");
const router = express.Router();
const path = require("path");
const fs = require("fs");

const upload = require("../middleware/uploadMiddleware");
const auth = require("../middleware/authMiddleware");

const {
  uploadResume,
  listUserResumes,
  getResume,
  deleteResume,
} = require("../controllers/resumeController");

const pythonService = require("../services/pythonService");

// ---------------- FILE SERVE (FIRST) ----------------
router.get("/file/:filename", (req, res) => {
  try {
    const filePath = path.join(
      __dirname,
      "../../uploads",
      req.params.filename
    );

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({
        success: false,
        message: "Resume file not found",
      });
    }

    res.setHeader("Content-Type", "application/pdf");
    res.sendFile(filePath);
  } catch (err) {
    console.error("Resume file serve error:", err);
    res.status(500).json({ success: false });
  }
});

// ---------------- UPLOAD ----------------
router.post("/upload", auth, upload.single("resume"), uploadResume);

// ---------------- AI ROUTES ----------------
router.post("/parse-text", auth, async (req, res) => {
  try {
    const { text, target_role } = req.body;
    const result = await pythonService.analyzeResume(text, target_role);
    return res.json({ success: true, data: result });
  } catch (err) {
    console.error("Parse-text error:", err);
    res.status(500).json({ message: "AI text parsing failed" });
  }
});

router.post("/roadmap", auth, async (req, res) => {
  try {
    const { skills, role } = req.body;
    const result = await pythonService.generateRoadmap(skills, role);
    return res.json(result);
  } catch (err) {
    res.status(500).json({ message: "AI roadmap generation failed" });
  }
});

router.post("/skill-gap", auth, async (req, res) => {
  try {
    const { resumeSkills, targetRole } = req.body;
    const result = await pythonService.skillGapAnalyzer(
      resumeSkills,
      targetRole
    );
    return res.json(result);
  } catch (err) {
    res.status(500).json({ message: "AI skill gap analysis failed" });
  }
});

// ---------------- CRUD (LAST) ----------------
router.get("/", auth, listUserResumes);
router.get("/:id", auth, getResume);
router.delete("/:id", auth, deleteResume);

module.exports = router;
