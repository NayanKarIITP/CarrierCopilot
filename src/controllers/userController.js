// const User = require("../models/user");

// // Get profile (protected route; authMiddleware must set req.user)
// exports.getProfile = async (req, res) => {
//   try {
//     const user = await User.findById(req.user._id).select("-password");
//     if (!user) return res.status(404).json({ success: false, message: "User not found" });
//     return res.json({ success: true, data: user });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// // Update profile (name, photoURL, etc.)
// exports.updateProfile = async (req, res) => {
//   try {
//     const updates = {};
//     const allowed = ["fullName", "photoURL", "lastLogin"];
//     allowed.forEach((k) => {
//       if (req.body[k] !== undefined) updates[k] = req.body[k];
//     });

//     const user = await User.findByIdAndUpdate(req.user._id, updates, { new: true }).select("-password");
//     return res.json({ success: true, data: user });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// // Change password (protected)
// exports.changePassword = async (req, res) => {
//   try {
//     const { currentPassword, newPassword } = req.body;
//     if (!currentPassword || !newPassword) return res.status(400).json({ success: false, message: "Both passwords required" });

//     const user = await User.findById(req.user._id);
//     const valid = await user.validatePassword(currentPassword);
//     if (!valid) return res.status(401).json({ success: false, message: "Current password incorrect" });

//     user.password = newPassword; // pre-save hook will hash
//     await user.save();
//     return res.json({ success: true, message: "Password updated" });
//   } catch (err) {
//     console.error(err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };







const User = require("../models/user");

// GET PROFILE
exports.getProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user._id).select("-password");
    return res.json({ success: true, data: user });
  } catch (err) {
    return res.status(500).json({ success: false, message: "Server Error" });
  }
};

exports.updateProfile = async (req, res) => {
  try {
    const { fullName, email, photoURL } = req.body;
    const updates = {};

    if (fullName) updates.fullName = fullName;
    if (email) updates.email = email;
    if (photoURL) updates.photoURL = photoURL;

    // Update and return the NEW document
    const user = await User.findByIdAndUpdate(req.user._id, updates, { new: true }).select("-password");

    return res.json({
      success: true,
      message: "Profile updated successfully",
      // ✅ FIX: Send back exactly what the context needs
      data: {
        id: user._id,
        fullName: user.fullName, // Match DB field
        email: user.email,
        photoURL: user.photoURL  // Match DB field
      }
    });
  } catch (err) {
    console.error("Update Error:", err);
    return res.status(500).json({ success: false, message: "Update failed" });
  }
};

// CHANGE PASSWORD
exports.changePassword = async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;

    const user = await User.findById(req.user._id);
    if (!user.password) {
      return res.status(400).json({ success: false, message: "Google accounts cannot change password here." });
    }

    const isMatch = await user.validatePassword(currentPassword);
    if (!isMatch) {
      return res.status(400).json({ success: false, message: "Incorrect current password" });
    }

    user.password = newPassword;
    await user.save();

    return res.json({ success: true, message: "Password updated successfully" });
  } catch (err) {
    return res.status(500).json({ success: false, message: "Server Error" });
  }
};