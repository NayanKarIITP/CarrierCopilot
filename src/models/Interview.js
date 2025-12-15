// const mongoose = require("mongoose");

// const interviewSchema = new mongoose.Schema(
//   {
//     userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
//     question: { type: String, required: true },
//     transcript: { type: String },
//     feedback: { type: Object }, // {filler_words, confidence, strengths, improvements}
//     createdAt: { type: Date, default: Date.now },
//   },
//   { timestamps: true }
// );

// module.exports = mongoose.model("Interview", interviewSchema);




const mongoose = require("mongoose");

const interviewSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    
    // ✅ CRITICAL ADDITION: This was missing!
    sessionId: { type: String, required: true, index: true },

    // ✅ ADDED: Needed for report header
    role: { type: String, default: "Software Engineer" },
    level: { type: String, default: "Mid-Level" },

    question: { type: String, required: true },
    transcript: { type: String },
    
    // ✅ RENAMED: Controller sends 'analysis', not 'feedback'
    analysis: { type: Object, default: {} }, 
    
    createdAt: { type: Date, default: Date.now },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Interview", interviewSchema);