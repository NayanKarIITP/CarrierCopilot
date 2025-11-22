const mongoose = require("mongoose");

const roadmapSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  targetRole: String,
  steps: Array,  // [{ step:1, title:"...", items:[...] }]
}, { timestamps: true });

module.exports = mongoose.model("Roadmap", roadmapSchema);
