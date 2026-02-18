
const Resume = require("../models/Resume");
const User = require("../models/user");
const Trends = require("../models/Trends"); 

exports.getDashboard = async (req, res) => {
  try {
    const userId = req.user._id;

    console.log("🟦 DASHBOARD REQUEST for User:", userId);

    // 1. Fetch User and latest Resume
    // We use .lean() for faster read-only access
    const user = await User.findById(userId).select("-password").lean();
    const latestResume = await Resume.findOne({ userId }).sort({ createdAt: -1 }).lean();

    if (!user) {
      return res.status(404).json({ success: false, message: "User not found" });
    }

    // 2. Prepare Data Sources
    // We prefer data from the Resume (most recent analysis), then fallback to User profile
    const gapsSource = latestResume?.gaps || user.skillGaps || [];
    
    // Roadmap can be an array or an object depending on how Python returned it.
    // We normalize it to ensure the frontend always gets the array it expects.
    let rawRoadmap = latestResume?.roadmap || user.learningRoadmap || user.roadmap || [];
    
    // If roadmap is wrapped in an object like { roadmap: [...] }, extract the array
    if (!Array.isArray(rawRoadmap) && rawRoadmap.roadmap) {
        rawRoadmap = rawRoadmap.roadmap;
    }

    // 3. Construct the Dashboard Data Object
    // This structure matches EXACTLY what your frontend components expect
    const dashboardData = {
      user: {
        fullName: user.fullName,
        email: user.email,
        photoURL: user.photoURL,
        targetRole: user.targetRole || "fullstack-developer"
      },
      
      resume: latestResume ? {
        uploaded: true,
        score: latestResume.score || 0,
        skills: latestResume.skills || [],
        gaps: gapsSource, // ✅ Critical: Sends the gaps to the frontend
        fileURL: latestResume.fileURL,
        updatedAt: latestResume.updatedAt,
        feedback: latestResume.feedback || [],
        strengths: latestResume.strengths || [],
        weaknesses: latestResume.weaknesses || []
      } : {
        uploaded: false,
        score: 0,
        skills: [],
        gaps: [],
        feedback: []
      },
      
      // Critical: Sends the roadmap to the frontend
      roadmap: {
        generated: rawRoadmap.length > 0,
        roadmap: rawRoadmap
      },
      
      // AI Tips: Combine feedback + specific tips if you have them
      aiTips: latestResume?.feedback || [
        "Upload a resume to get started.",
        "Complete your profile for better recommendations."
      ],
      
      trends: [] // Placeholder for trends if you implement them later
    };

    return res.json({
      success: true,
      data: dashboardData
    });

  } catch (err) {
    console.error("❌ Dashboard Error:", err);
    return res.status(500).json({ success: false, message: "Server Error" });
  }
};