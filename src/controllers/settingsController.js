const Settings = require("../models/Settings");

// Get settings for the user (or default)

exports.getSettings = async (req, res) => {
  try {
    let settings = await Settings.findOne({ userId: req.user._id });
    if (!settings) {
      // return defaults
      return res.json({
        success: true,
        data: {
          emailNotifications: true,
          performanceAlerts: true,
          weeklySummary: false,
          goalReminder: true,
          theme: "light",
        },
      });
    }
    return res.json({ success: true, data: settings });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// Update or create settings

exports.updateSettings = async (req, res) => {
  try {
    const updates = req.body;
    let settings = await Settings.findOneAndUpdate({ userId: req.user._id }, updates, { new: true, upsert: true });
    return res.json({ success: true, data: settings });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};
