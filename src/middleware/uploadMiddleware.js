

//for production with cloudinary
const multer = require("multer");
const { storage } = require("../config/cloudinary"); // Import the config we made earlier

// NEW: Use Cloudinary Storage
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