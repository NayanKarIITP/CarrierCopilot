

const mongoose = require("mongoose");

const roadmapSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  targetRole: String,
  
  // NEW: Store the level (Beginner/Intermediate/Advanced)
  level: { type: String, default: "Beginner" },
  
  // NEW: Store the skills used to generate this roadmap
  currentSkills: [String],

  // Stores the array of steps/cards
  steps: Array, 
}, { timestamps: true });

module.exports = mongoose.model("Roadmap", roadmapSchema);