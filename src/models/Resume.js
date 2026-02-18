const mongoose = require("mongoose");

// Optional: Define a sub-schema for Roadmap to ensure data consistency
const roadmapItemSchema = new mongoose.Schema({
  skill: { type: String, required: true },
  description: String,
  resources: [String], // Array of URLs or book titles
  status: { 
    type: String, 
    enum: ["pending", "in-progress", "completed"], 
    default: "pending" 
  },
  deadline: Date
}, { _id: false }); // _id is usually not needed for sub-documents unless i update them individually

const resumeSchema = new mongoose.Schema({
  userId: { 
    type: mongoose.Schema.Types.ObjectId, 
    ref: "User", 
    required: true,
    index: true // Optimizes lookup queries
  },

  // 1. Basic Info
  rawText: { type: String }, // Stores full text for re-parsing if needed
  skills: [{ type: String, trim: true }],

  // 2. Education
  education: [
    {
      degree: { type: String, trim: true },
      school: { type: String, trim: true },
      year: { type: String, trim: true }, // Keeping as String is good for ranges like "2020-2024"
    }
  ],

  // 3. Experience 
  experience: [
    {
      title: { type: String, trim: true },
      company: { type: String, trim: true },
      dates: { type: String, trim: true },
      bullets: [{ type: String, trim: true }],
    }
  ],

  // 4. Analysis Data (AI Generated)
  score: { type: Number, default: 0, min: 0, max: 100 },
  feedback: [String],
  strengths: [String],
  weaknesses: [String],

  // CRITICAL: Gap Analysis & Learning Path
  gaps: [String],
  
  // Using the sub-schema defined above for stricter validation
  // If i want to prefer loose structure, keep it as [Object]
  roadmap: [roadmapItemSchema], 

  // Cloudinary Info
  fileURL: { type: String, required: true },
  fileId: { type: String } // Useful for deleting the file from Cloudinary later
}, { timestamps: true });

module.exports = mongoose.model("Resume", resumeSchema);

