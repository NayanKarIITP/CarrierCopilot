// const mongoose = require("mongoose");


// const resumeSchema = new mongoose.Schema({
//   userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
//   rawText: String,
//   skills: [String],
//   education: [String],
//   experience: [String],
//   score: Number,
//   feedback: [String],
//   fileURL: String,
// }, { timestamps: true });

// module.exports = mongoose.model("Resume", resumeSchema);





const mongoose = require("mongoose");

const resumeSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  
  // 1. Basic Info
  rawText: String,
  skills: [String],

  // 2. Education (Updated to match Python output keys)
  education: [
    {
      degree: String,
      school: String, // Python sends 'school', not 'institution'
      year: String,
    }
  ],

  // 3. Experience (Updated to match Python output keys)
  experience: [
    {
      title: String,
      company: String,
      dates: String,   // Python sends 'dates', not 'duration'
      bullets: [String], // Python sends an array of strings called 'bullets'
    }
  ],

  // 4. Analysis Data
  score: { type: Number, default: 0 },
  feedback: [String],
  
  // ✅ NEW: Added these to store the strengths/weaknesses we calculate in the controller
  strengths: [String],
  weaknesses: [String],

  fileURL: String,
}, { timestamps: true });

module.exports = mongoose.model("Resume", resumeSchema);