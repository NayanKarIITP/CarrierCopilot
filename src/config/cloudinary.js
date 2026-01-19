// src/config/cloudinary.js
const cloudinary = require('cloudinary').v2;
const { CloudinaryStorage } = require('multer-storage-cloudinary');
require('dotenv').config();

// 1. Setup Credentials
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

// 2. Setup Storage Engine
const storage = new CloudinaryStorage({
  cloudinary: cloudinary,
  params: {
    folder: 'career-copilot-resumes', // Folder name in your Cloudinary Dashboard
    allowed_formats: ['pdf', 'doc', 'docx'],
    resource_type: 'raw', // 'raw' is CRITICAL for PDF files!
  },
});

module.exports = { storage };