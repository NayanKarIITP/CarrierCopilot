const User = require("../models/user");
const Resume = require("../models/Resume");
const Roadmap = require("../models/Roadmap");
const Trends = require("../models/Trends");

exports.getDashboard = async (req, res) => {
  try {
    const user = await User.findById(req.user._id).select("-password");

    const latestResume = await Resume.findOne({ userId: req.user._id })
      .sort({ createdAt: -1 });

    const roadmap = await Roadmap.findOne({ userId: req.user._id })
      .sort({ createdAt: -1 });

    const trends = await Trends.findOne().sort({ createdAt: -1 });

    return res.json({
      success: true,
      data: {
        user: {
          fullName: user.fullName,
          photoURL: user.photoURL,
          lastLogin: user.lastLogin,
        },

        resume: {
          uploaded: user.resumeUploaded,
          score: user.resumeScore,
          skills: user.extractedSkills,
          gaps: user.skillGaps,
          latestResume,
        },

        roadmap: {
          generated: user.roadmapGenerated,
          roadmap,
        },

        trends: trends || null,

        stats: {
          totalUploads: await Resume.countDocuments({ userId: req.user._id }),
          totalInterviews: 0, // will add later if needed
        }
      }
    });

  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Dashboard fetch error" });
  }
};
