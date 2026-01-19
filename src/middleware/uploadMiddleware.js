//for local testing purposes only
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



//for production with cloudinary
const multer = require("multer");
const { storage } = require("../config/cloudinary"); // Import the config we made earlier

// ✅ NEW: Use Cloudinary Storage
const upload = multer({
  storage: storage, // Uses the Cloudinary engine
  limits: { fileSize: 10 * 1024 * 1024 }, // Limit to 10 MB
  fileFilter: (req, file, cb) => {
    // Basic check for PDF/Docs
    if (file.mimetype === "application/pdf" || 
        file.mimetype === "application/msword" || 
        file.mimetype === "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
        file.mimetype === "text/plain") {
      cb(null, true);
    } else {
      cb(new Error("Invalid file type. Only PDF/DOC/DOCX/TXT allowed."), false);
    }
  }
});

module.exports = upload;