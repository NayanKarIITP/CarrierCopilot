const mongoose = require("mongoose");


const resumeSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  rawText: String,
  skills: [String],
  education: [String],
  experience: [String],
  score: Number,
  feedback: [String],
  fileURL: String,
}, { timestamps: true });

module.exports = mongoose.model("Resume", resumeSchema);
