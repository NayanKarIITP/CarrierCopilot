const User = require("../models/user");

// Get profile (protected route; authMiddleware must set req.user)
exports.getProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user._id).select("-password");
    if (!user) return res.status(404).json({ success: false, message: "User not found" });
    return res.json({ success: true, data: user });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// Update profile (name, photoURL, etc.)
exports.updateProfile = async (req, res) => {
  try {
    const updates = {};
    const allowed = ["fullName", "photoURL", "lastLogin"];
    allowed.forEach((k) => {
      if (req.body[k] !== undefined) updates[k] = req.body[k];
    });

    const user = await User.findByIdAndUpdate(req.user._id, updates, { new: true }).select("-password");
    return res.json({ success: true, data: user });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// Change password (protected)
exports.changePassword = async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    if (!currentPassword || !newPassword) return res.status(400).json({ success: false, message: "Both passwords required" });

    const user = await User.findById(req.user._id);
    const valid = await user.validatePassword(currentPassword);
    if (!valid) return res.status(401).json({ success: false, message: "Current password incorrect" });

    user.password = newPassword; // pre-save hook will hash
    await user.save();
    return res.json({ success: true, message: "Password updated" });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};
