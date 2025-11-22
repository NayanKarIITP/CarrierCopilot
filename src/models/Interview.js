const mongoose = require("mongoose");

const interviewSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    question: { type: String, required: true },
    transcript: { type: String },
    feedback: { type: Object }, // {filler_words, confidence, strengths, improvements}
    createdAt: { type: Date, default: Date.now },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Interview", interviewSchema);
