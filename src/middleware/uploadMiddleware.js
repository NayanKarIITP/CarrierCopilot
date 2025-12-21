// const multer = require("multer");
// const path = require("path");
// const fs = require("fs");

// // ensure upload dir exists
// const uploadDir = path.join(__dirname, "..", "uploads", "resumes");
// if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

// // allowed file extensions
// const ALLOWED_EXTS = ['.pdf', '.doc', '.docx', '.txt'];

// const storage = multer.diskStorage({
//   destination: function (req, file, cb) {
//     cb(null, uploadDir);
//   },
//   filename: function (req, file, cb) {
//     const safeName = file.originalname.replace(/\s+/g, "_");
//     cb(null, `${Date.now()}-${safeName}`);
//   },
// });

// function fileFilter(req, file, cb) {
//   const ext = path.extname(file.originalname).toLowerCase();
//   if (!ALLOWED_EXTS.includes(ext)) {
//     return cb(new Error("Invalid file type. Only PDF/DOC/DOCX/TXT allowed."));
//   }
//   cb(null, true);
// }

// const upload = multer({
//   storage,
//   limits: { fileSize: 12 * 1024 * 1024 }, // 12 MB
//   fileFilter,
// });

// module.exports = upload;





// src/middleware/uploadMiddleware.js

const multer = require("multer");

/**
 * ✅ MEMORY STORAGE (RENDER + SERVERLESS SAFE)
 * - No disk writes
 * - req.file.buffer available
 */
const storage = multer.memoryStorage();

const upload = multer({
  storage,
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype !== "application/pdf") {
      return cb(new Error("Only PDF files are allowed"), false);
    }
    cb(null, true);
  },
});

module.exports = upload;
