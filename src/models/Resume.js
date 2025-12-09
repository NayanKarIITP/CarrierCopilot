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
  rawText: String,
  
  skills: [String],

  // CHANGE THESE 👇
  education: [
    {
      degree: String,
      institution: String,
      year: String,
    }
  ],

  experience: [
    {
      title: String,
      company: String,
      duration: String,
      description: String,
    }
  ],

  score: Number,
  feedback: [String],
  fileURL: String,
}, { timestamps: true });

module.exports = mongoose.model("Resume", resumeSchema);
