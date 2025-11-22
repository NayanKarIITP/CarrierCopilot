const mongoose = require("mongoose");

const settingsSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },

  emailNotifications: { type: Boolean, default: true },
  performanceAlerts: { type: Boolean, default: true },
  weeklySummary: { type: Boolean, default: false },
  goalReminder: { type: Boolean, default: true },

  theme: { type: String, enum: ["light", "dark"], default: "light" },
}, { timestamps: true });

module.exports = mongoose.model("Settings", settingsSchema);
