// // services/pythonService.js
// const axios = require("axios");

// // ---------------------------------------------------------
// // 🔧 CONFIGURATION
// // ---------------------------------------------------------
// // Default to localhost for testing if ENV is missing
// const PYTHON_API_URL = process.env.PYTHON_SERVICE_URL || "https://carriercopilot.onrender.com";

// console.log(`🔌 Connecting to Python Engine at: ${PYTHON_API_URL}`);

// /* ================== RESUME ================== */

// /**
//  * 🔹 Sends Cloudinary URL to Python
//  * ✅ Added 60s timeout to prevent frontend crash during AI analysis
//  */
// async function processResume(fileUrl, targetRole = "fullstack-developer") {
//   try {
//     console.log(`🔗 Sending URL to Python: ${fileUrl}`);

//     const res = await axios.post(`${PYTHON_API_URL}/resume/parse`, {
//       url: fileUrl,
//       target_role: targetRole
//     }, {
//       timeout: 60000 // ⏳ Wait up to 60 seconds
//     });

//     return res.data;
//   } catch (err) {
//     console.error("❌ PYTHON PARSE ERROR:", err?.response?.data || err.message);
//     // Return a safe error object so the frontend doesn't crash
//     return { success: false, error: "AI Service Timeout or Failed" };
//   }
// }

// // Note: /resume/analyze (Text) is not currently in your Python app.
// // Leaving it here in case you add it later, but generally unused now.
// async function analyzeResume(text, targetRole = null) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/resume/analyze`, {
//       text,
//       target_role: targetRole || null
//     });
//     return res.data;
//   } catch (err) {
//     console.error("❌ PYTHON ANALYZE ERROR:", err.message);
//     return { success: false };
//   }
// }


// /* ================== ROADMAP ================== */

// /**
//  * ✅ Added 60s timeout for Roadmap generation
//  */
// async function generateRoadmap(skills, role) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/roadmap/generate`, {
//       skills,
//       role
//     }, {
//       timeout: 60000 // ⏳ Wait up to 60 seconds
//     });

//     if (!res.data || !res.data.roadmap) {
//       throw new Error("Python returned empty roadmap");
//     }

//     return res.data;

//   } catch (err) {
//     console.error("❌ PYTHON ROADMAP ERROR:", err?.response?.data || err.message);
//     return null;   // Clean fallback
//   }
// }


// async function skillGapAnalyzer(resumeSkills, targetRole) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/roadmap/gap`, {
//       current_skills: resumeSkills,
//       target_role: targetRole
//     });
//     return res.data;
//   } catch (err) {
//     console.error("❌ SKILL GAP ERROR:", err.message);
//     return null;
//   }
// }

// async function getMarketTrends() {
//   try {
//     const res = await axios.get(`${PYTHON_API_URL}/trends`);
//     return res.data;
//   } catch (err) {
//     console.error("❌ TRENDS ERROR:", err.message);
//     return [];
//   }
// }


// /* ================== INTERVIEW ENGINE ================== */

// async function getInterviewQuestion(role, level, sessionId = null) {
//   try {
//     let endpoint = "/interview/start";
//     let body = { role, level };

//     if (sessionId) {
//       endpoint = "/interview/next-question";
//       body.sessionId = sessionId;
//     }
//     const res = await axios.post(`${PYTHON_API_URL}${endpoint}`, body);
//     return res.data?.question || null;
//   } catch (err) {
//     console.error("❌ INTERVIEW Q ERROR:", err.message);
//     return null;
//   }
// }

// async function analyzeInterview(transcript) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, {
//       transcript
//     });
//     return res.data?.data?.analysis;
//   } catch (err) {
//     console.error("❌ INTERVIEW ANALYZE ERROR:", err.message);
//     return null;
//   }
// }

// async function getFrameMetrics(imageBase64) {
//   try {
//     const res = await axios.post(
//       `${PYTHON_API_URL}/interview/frame-metrics`,
//       { image_base64: imageBase64 }
//     );
//     return res.data?.metrics;
//   } catch (err) {
//     console.error("❌ FRAME METRICS ERROR:", err.message);
//     return null;
//   }
// }


// /* ================== EXPORT ================== */
// module.exports = {
//   processResume,
//   analyzeResume,
//   generateRoadmap,
//   skillGapAnalyzer,
//   getMarketTrends,
//   getInterviewQuestion,
//   analyzeInterview,
//   getFrameMetrics,
// };






//pythonService.js
const axios = require("axios");

// ---------------------------------------------------------
// 🔧 CONFIGURATION
// ---------------------------------------------------------
// Default to localhost for testing if ENV is missing
const PYTHON_API_URL = process.env.PYTHON_SERVICE_URL || "https://carriercopilot-nk.onrender.com";

console.log(`🔌 Connecting to Python Engine at: ${PYTHON_API_URL}`);

/* ================== RESUME ================== */

/**
 * 🔹 Sends Cloudinary URL to Python
 * ✅ Added 60s timeout to prevent frontend crash during AI analysis
 */
async function processResume(fileUrl, targetRole = "fullstack-developer") {
  try {
    console.log(`🔗 Sending URL to Python: ${fileUrl}`);

    const res = await axios.post(`${PYTHON_API_URL}/resume/parse`, {
      url: fileUrl,
      target_role: targetRole
    }, {
      timeout: 60000 // ⏳ Wait up to 60 seconds
    });

    return res.data;
  } catch (err) {
    console.error("❌ PYTHON PARSE ERROR:", err?.response?.data || err.message);
    // Return a safe error object so the frontend doesn't crash
    return { success: false, error: "AI Service Timeout or Failed" };
  }
}

// Note: /resume/analyze (Text) is not currently in your Python app.
async function analyzeResume(text, targetRole = null) {
  try {
    const res = await axios.post(`${PYTHON_API_URL}/resume/analyze`, {
      text,
      target_role: targetRole || null
    });
    return res.data;
  } catch (err) {
    console.error("❌ PYTHON ANALYZE ERROR:", err.message);
    return { success: false };
  }
}


/* ================== ROADMAP ================== */

/**
 * ✅ Added 60s timeout for Roadmap generation
 */
async function generateRoadmap(skills, role) {
  try {
    const res = await axios.post(`${PYTHON_API_URL}/roadmap/generate`, {
      skills,
      role
    }, {
      timeout: 60000 // ⏳ Wait up to 60 seconds
    });

    if (!res.data || !res.data.roadmap) {
      throw new Error("Python returned empty roadmap");
    }

    return res.data;

  } catch (err) {
    console.error("❌ PYTHON ROADMAP ERROR:", err?.response?.data || err.message);
    return null;   // Clean fallback
  }
}

/**
 * ✅ FIXED: Added 60s timeout for Skill Gap Analysis
 * This was likely timing out on Render (causing empty boxes)
 */
async function skillGapAnalyzer(resumeSkills, targetRole) {
  try {
    const res = await axios.post(`${PYTHON_API_URL}/roadmap/gap`, {
      current_skills: resumeSkills,
      target_role: targetRole
    }, {
      timeout: 60000 // ⏳ Wait up to 60 seconds (Fix for Render)
    });
    return res.data;
  } catch (err) {
    console.error("❌ SKILL GAP ERROR:", err.message);
    return { missing_skills: [] }; // Return valid structure on error
  }
}

async function getMarketTrends() {
  try {
    const res = await axios.get(`${PYTHON_API_URL}/trends`, {
        timeout: 10000 // Short timeout for trends is usually fine
    });
    return res.data;
  } catch (err) {
    console.error("❌ TRENDS ERROR:", err.message);
    return [];
  }
}


/* ================== INTERVIEW ENGINE ================== */

async function getInterviewQuestion(role, level, sessionId = null) {
  try {
    let endpoint = "/interview/start";
    let body = { role, level };

    if (sessionId) {
      endpoint = "/interview/next-question";
      body.sessionId = sessionId;
    }
    const res = await axios.post(`${PYTHON_API_URL}${endpoint}`, body);
    return res.data?.question || null;
  } catch (err) {
    console.error("❌ INTERVIEW Q ERROR:", err.message);
    return null;
  }
}

async function analyzeInterview(transcript) {
  try {
    const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, {
      transcript
    });
    return res.data?.data?.analysis;
  } catch (err) {
    console.error("❌ INTERVIEW ANALYZE ERROR:", err.message);
    return null;
  }
}

async function getFrameMetrics(imageBase64) {
  try {
    const res = await axios.post(
      `${PYTHON_API_URL}/interview/frame-metrics`,
      { image_base64: imageBase64 }
    );
    return res.data?.metrics;
  } catch (err) {
    console.error("❌ FRAME METRICS ERROR:", err.message);
    return null;
  }
}


/* ================== EXPORT ================== */
module.exports = {
  processResume,
  analyzeResume,
  generateRoadmap,
  skillGapAnalyzer,
  getMarketTrends,
  getInterviewQuestion,
  analyzeInterview,
  getFrameMetrics,
};






// //For production
// const axios = require("axios");

// const PYTHON_API_URL =
//   process.env.PYTHON_SERVICE_URL || "https://carriercopilot.onrender.com";

// /* ================== RESUME ================== */

// /**
//  * 🔹 UPDATED: Sends Cloudinary URL to Python instead of File Stream
//  */
// async function processResume(fileUrl, targetRole = "fullstack-developer") {
//   try {
//     console.log(`🔗 sending URL to Python: ${fileUrl}`);

//     const res = await axios.post(`${PYTHON_API_URL}/resume/parse`, {
//       url: fileUrl,
//       target_role: targetRole
//     });

//     return res.data;
//   } catch (err) {
//     console.error("❌ PYTHON PARSE ERROR:", err?.response?.data || err.message);
//     return { success: false, error: "AI Service Failed" };
//   }
// }

// async function analyzeResume(text, targetRole = null) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/resume/analyze`, {
//       text,
//       target_role: targetRole || null
//     });
//     return res.data;
//   } catch (err) {
//     console.error("❌ PYTHON ANALYZE ERROR:", err.message);
//     return { success: false };
//   }
// }


// /* ================== ROADMAP ================== */
// async function generateRoadmap(skills, role) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/roadmap/generate`, {
//       skills,
//       role
//     });

//     if (!res.data || !res.data.roadmap) {
//       throw new Error("Python returned empty roadmap");
//     }

//     return res.data;

//   } catch (err) {
//     console.error("❌ PYTHON ROADMAP ERROR:", err?.response?.data || err.message);
//     return null;   // <-- clean fallback trigger
//   }
// }


// async function skillGapAnalyzer(resumeSkills, targetRole) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/roadmap/gap`, {
//       current_skills: resumeSkills,
//       target_role: targetRole
//     });
//     return res.data;
//   } catch (err) {
//     console.error("❌ SKILL GAP ERROR:", err.message);
//     return null;
//   }
// }

// async function getMarketTrends() {
//   try {
//     const res = await axios.get(`${PYTHON_API_URL}/trends`);
//     return res.data;
//   } catch (err) {
//     console.error("❌ TRENDS ERROR:", err.message);
//     return [];
//   }
// }


// /* ---------------------------------------------------
//    INTERVIEW ENGINE
// --------------------------------------------------- */

// async function getInterviewQuestion(role, level, sessionId = null) {
//   try {
//     let endpoint = "/interview/start";
//     let body = { role, level };

//     if (sessionId) {
//       endpoint = "/interview/next-question";
//       body.sessionId = sessionId;
//     }
//     const res = await axios.post(`${PYTHON_API_URL}${endpoint}`, body);
//     return res.data?.question || null;
//   } catch (err) {
//     console.error("❌ INTERVIEW Q ERROR:", err.message);
//     return null;
//   }
// }

// async function analyzeInterview(transcript) {
//   try {
//     const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, {
//       transcript
//     });
//     return res.data?.data?.analysis;
//   } catch (err) {
//     console.error("❌ INTERVIEW ANALYZE ERROR:", err.message);
//     return null;
//   }
// }

// async function getFrameMetrics(imageBase64) {
//   try {
//     const res = await axios.post(
//       `${PYTHON_API_URL}/interview/frame-metrics`,
//       { image_base64: imageBase64 }
//     );
//     return res.data?.metrics;
//   } catch (err) {
//     console.error("❌ FRAME METRICS ERROR:", err.message);
//     return null;
//   }
// }


// /* ================== EXPORT ================== */
// module.exports = {
//   processResume,
//   analyzeResume,
//   generateRoadmap,
//   skillGapAnalyzer,
//   getMarketTrends,
//   getInterviewQuestion,
//   analyzeInterview,
//   getFrameMetrics,
// };