// // src/controllers/interviewController.js
// const Interview = require("../models/Interview");
// const pythonService = require("../services/pythonService");

// /**
//  * Fetch a new interview question (Python Microservice)
//  */
// exports.getQuestion = async (req, res) => {
//   try {
//     const q = await pythonService.getInterviewQuestion();

//     return res.json({
//       success: true,
//       question: q.question,
//       follow_up: q.follow_up,
//       difficulty: q.difficulty,
//     });
//   } catch (err) {
//     console.error("Interview Question Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * Analyze the transcript (answer) of the candidate
//  */
// exports.analyze = async (req, res) => {
//   try {
//     console.log("REQ BODY →", req.body);
//     const { transcript, question } = req.body;

//     if (!transcript) {
//       return res
//         .status(400)
//         .json({ success: false, message: "Transcript is required" });
//     }

//     // Call Python microservice
//     const analysis = await pythonService.analyzeInterview(transcript);

//     // Save session ONLY if logged in
//     let session = null;
//     if (req.user) {
//       session = await Interview.create({
//         userId: req.user._id,
//         question: question || "",
//         transcript,
//         analysis,
//       });
//     }

//     return res.json({
//       success: true,
//       data: {
//         analysis,
//         session,
//       },
//     });
//   } catch (err) {
//     console.error("Interview Analysis Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * List all interview sessions of logged-in user
//  */
// exports.listSessions = async (req, res) => {
//   try {
//     const sessions = await Interview.find({ userId: req.user._id }).sort({
//       createdAt: -1,
//     });

//     return res.json({ success: true, data: sessions });
//   } catch (err) {
//     console.error("List Sessions Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };










// // src/controllers/interviewController.js
// const Interview = require("../models/Interview");
// const pythonService = require("../services/pythonService");

// /**
//  * 1. Start a New Session (Initialize)
//  */
// exports.startSession = async (req, res) => {
//   try {
//     const { role } = req.body;
//     // You could create a DB record here if you want to track session history
//     const sessionId = Date.now().toString(); // Simple ID for now
    
//     return res.json({ 
//       success: true, 
//       sessionId, 
//       message: `Interview session started for ${role}` 
//     });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: err.message });
//   }
// };

// /**
//  * 2. Fetch a New Question (Python Microservice)
//  */
// exports.getQuestion = async (req, res) => {
//   try {
//     const { role } = req.body; // Can be passed from frontend
//     const q = await pythonService.getInterviewQuestion(role || "fullstack-developer");

//     return res.json({
//       success: true,
//       question: {
//         _id: Date.now().toString(),
//         text: q.question,
//         followUp: q.follow_up,
//         difficulty: q.difficulty,
//       }
//     });
//   } catch (err) {
//     console.error("Interview Question Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * 3. Analyze Transcript (Audio/Text)
//  */
// exports.analyze = async (req, res) => {
//   try {
//     const { transcript, question } = req.body;

//     if (!transcript) {
//       return res.status(400).json({ success: false, message: "Transcript is required" });
//     }

//     // Call Python microservice
//     const analysis = await pythonService.analyzeInterview(transcript);

//     // Save session ONLY if logged in
//     let session = null;
//     if (req.user) {
//       session = await Interview.create({
//         userId: req.user._id,
//         question: question || "",
//         transcript,
//         analysis,
//       });
//     }

//     return res.json({
//       success: true,
//       data: {
//         analysis,
//         session,
//       },
//     });
//   } catch (err) {
//     console.error("Interview Analysis Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * 4. Get Frame Metrics (Video Analysis) - MISSING PART FIXED
//  */
// exports.getFrameMetrics = async (req, res) => {
//   try {
//     const { image } = req.body; // Expecting base64 image string
//     if (!image) return res.status(400).json({ success: false, message: "No image data" });

//     // Call Python Service (face_engine.py)
//     // Note: You need to ensure pythonService.js has this function exposed
//     const metrics = await pythonService.analyzeFrame(image);

//     return res.json({ success: true, metrics });
//   } catch (err) {
//     console.error("Frame Metrics Error:", err);
//     // Return default/empty metrics so frontend doesn't crash
//     return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });
//   }
// };

// /**
//  * 5. List Sessions
//  */
// exports.listSessions = async (req, res) => {
//   try {
//     const sessions = await Interview.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: sessions });
//   } catch (err) {
//     console.error("List Sessions Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };







// // src/controllers/interviewController.js
// const Interview = require("../models/Interview");
// const pythonService = require("../services/pythonService");

// /**
//  * 1. Start a New Session (Initialize)
//  */
// exports.startSession = async (req, res) => {
//   try {
//     // ✅ Receive both Role and Level from Frontend
//     const { role, level } = req.body; 
//     const sessionId = Date.now().toString(); // Simple ID for now
    
//     return res.json({ 
//       success: true, 
//       sessionId, 
//       message: `Interview session started for ${level || "Mid-Level"} ${role || "Candidate"}` 
//     });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: err.message });
//   }
// };

// /**
//  * 2. Fetch a New Question (Python Microservice)
//  */
// exports.getQuestion = async (req, res) => {
//   try {
//     // ✅ Extract role and level from request body
//     const { role, level } = req.body; 
    
//     // ✅ Pass both to Python service
//     // If frontend sends nothing, default to Software Engineer / Mid-Level
//     const q = await pythonService.getInterviewQuestion(
//         role || "Software Engineer", 
//         level || "Mid-Level"
//     );

//     return res.json({
//       success: true,
//       question: {
//         _id: Date.now().toString(),
//         text: q.question,
//         followUp: q.follow_up,
//         difficulty: q.difficulty,
//       }
//     });
//   } catch (err) {
//     console.error("Interview Question Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * 3. Analyze Transcript (Audio/Text)
//  */
// exports.analyze = async (req, res) => {
//   try {
//     const { transcript, question } = req.body;

//     if (!transcript) {
//       return res.status(400).json({ success: false, message: "Transcript is required" });
//     }

//     // Call Python microservice
//     const analysis = await pythonService.analyzeInterview(transcript);

//     // Save session ONLY if logged in
//     let session = null;
//     if (req.user) {
//       session = await Interview.create({
//         userId: req.user._id,
//         question: question || "",
//         transcript,
//         analysis,
//       });
//     }

//     return res.json({
//       success: true,
//       data: {
//         analysis,
//         session,
//       },
//     });
//   } catch (err) {
//     console.error("Interview Analysis Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * 4. Get Frame Metrics (Video Analysis)
//  */
// exports.getFrameMetrics = async (req, res) => {
//   try {
//     const { image } = req.body; // Expecting base64 image string
//     if (!image) return res.status(400).json({ success: false, message: "No image data" });

//     // Call Python Service (face_engine.py)
//     const metrics = await pythonService.analyzeFrame(image);

//     return res.json({ success: true, metrics });
//   } catch (err) {
//     console.error("Frame Metrics Error:", err);
//     // Return default/empty metrics so frontend doesn't crash
//     return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });
//   }
// };

// /**
//  * 5. List Sessions
//  */
// exports.listSessions = async (req, res) => {
//   try {
//     const sessions = await Interview.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: sessions });
//   } catch (err) {
//     console.error("List Sessions Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };








// // src/controllers/interviewController.js
// const Interview = require("../models/Interview");
// const pythonService = require("../services/pythonService");

// // ... (Keep startSession, getQuestion, analyze, getFrameMetrics as they are) ...

// exports.startSession = async (req, res) => {
//   try {
//     const { role, level } = req.body; 
//     const sessionId = Date.now().toString();
//     return res.json({ success: true, sessionId, message: `Started` });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: err.message });
//   }
// };

// exports.getQuestion = async (req, res) => {
//   try {
//     const { role, level } = req.body; 
//     const q = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");
//     return res.json({
//       success: true,
//       question: { _id: Date.now().toString(), text: q.question, followUp: q.follow_up, difficulty: q.difficulty }
//     });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// exports.analyze = async (req, res) => {
//   try {
//     const { transcript, question } = req.body;
//     if (!transcript) return res.status(400).json({ success: false, message: "Transcript required" });

//     const analysis = await pythonService.analyzeInterview(transcript);
//     let session = null;
    
//     // ✅ Save to DB so we can load it in the Performance Page
//     if (req.user) {
//       session = await Interview.create({
//         userId: req.user._id,
//         question: question || "",
//         transcript,
//         analysis,
//       });
//     }
//     return res.json({ success: true, data: { analysis, session } });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// exports.getFrameMetrics = async (req, res) => {
//   try {
//     const { image } = req.body; 
//     if (!image) return res.status(400).json({ success: false, message: "No image data" });
//     const metrics = await pythonService.analyzeFrame(image);
//     return res.json({ success: true, metrics });
//   } catch (err) {
//     return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });
//   }
// };

// // NEW: Get a single session by ID (for Performance Page)
// exports.getQuestion = async (req, res) => {
//   try {
//     const { role, level } = req.body; 
//     const response = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");

//     // ✅ UNPACK DATA SAFELY
//     let questionData = response;
    
//     // If the python service returns { question: { question: "..." } }
//     if (response.question && typeof response.question === 'object') {
//         questionData = response.question;
//     }

//     return res.json({
//       success: true,
//       question: {
//         _id: Date.now().toString(),
//         text: questionData.question, // This will now always be a string
//         followUp: questionData.follow_up,
//         difficulty: questionData.difficulty,
//       }
//     });
//   } catch (err) {
//     console.error("Interview Question Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// exports.listSessions = async (req, res) => {
//   try {
//     const sessions = await Interview.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: sessions });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };







// // src/controllers/interviewController.js
// const Interview = require("../models/Interview");
// const pythonService = require("../services/pythonService");

// /**
//  * 1. Start a New Interview Session
//  * Generates an ID and fetches the FIRST question immediately.
//  */
// exports.startSession = async (req, res) => {
//   try {
//     const { role, level } = req.body;
//     const sessionId = Date.now().toString();

//     console.log(`🚀 Starting session for ${role} (${level})...`);

//     // 1. Call Python Service
//     const q = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");

//     // 🛡️ CRASH FIX: Check if q is null before accessing properties
//     if (!q) {
//         console.error("❌ Python Service returned null. Using fallback.");
        
//         return res.json({
//             success: true,
//             sessionId,
//             question: {
//                 _id: Date.now().toString(),
//                 text: "Could not generate a specific question. Please tell me about your background and core skills.", 
//                 followUp: "What is your strongest programming language?",
//                 difficulty: level || "Mid-Level"
//             }
//         });
//     }

//     // 2. Return Valid Data
//     return res.json({
//       success: true,
//       sessionId,
//       question: {
//         _id: Date.now().toString(),
//         text: q.question || q.text || "Tell me about yourself.",
//         followUp: q.follow_up || q.followUp || "",
//         difficulty: q.difficulty || level
//       }
//     });

//   } catch (err) {
//     console.error("🔥 Start Session Error:", err);
//     // Return 500 so the frontend handles it gracefully without the server dying
//     return res.status(500).json({ success: false, message: "Failed to start session" });
//   }
// };

// /**
//  * 2. Get Next Question
//  * Called when user clicks "Next Question"
//  */
// exports.getQuestion = async (req, res) => {
//   try {
//     const { role, level } = req.body; 
    
//     const response = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");

//     // 🛡️ CRASH FIX: Handle null response
//     if (!response) {
//         return res.json({
//             success: true,
//             question: {
//                 _id: Date.now().toString(),
//                 text: "Describe a challenging technical problem you solved.",
//                 followUp: "How did you debug it?",
//                 difficulty: level,
//             }
//         });
//     }

//     // Robust Data Unpacking
//     let questionText = response.question || "Could not generate question.";
//     let followUpText = response.follow_up || "";

//     if (typeof response.question === 'object') {
//         questionText = response.question.question;
//         followUpText = response.question.follow_up;
//     }

//     return res.json({
//       success: true,
//       question: {
//         _id: Date.now().toString(),
//         text: questionText,
//         followUp: followUpText,
//         difficulty: response.difficulty || level,
//       }
//     });

//   } catch (err) {
//     console.error("Get Question Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };

// /**
//  * 3. Analyze Answer
//  * Process transcript with AI
//  */
// exports.analyze = async (req, res) => {
//   try {
//     const { transcript, question } = req.body;
    
//     if (!transcript) {
//         return res.status(400).json({ success: false, message: "Transcript required" });
//     }

//     const analysis = await pythonService.analyzeInterview(transcript);
    
//     // Optional: Save to DB
//     let session = null;
//     if (req.user) {
//       try {
//           session = await Interview.create({
//             userId: req.user._id,
//             question: question || "Unknown",
//             transcript,
//             analysis: analysis || {}, // Ensure analysis isn't null
//           });
//       } catch (dbErr) {
//           console.warn("⚠️ Failed to save to DB:", dbErr.message);
//       }
//     }

//     return res.json({ 
//         success: true, 
//         data: { analysis: analysis || {}, session } 
//     });

//   } catch (err) {
//     console.error("Analysis Error:", err);
//     return res.status(500).json({ success: false, message: "Analysis failed" });
//   }
// };

// /**
//  * 4. Frame Metrics (Video Analysis)
//  */
// exports.getFrameMetrics = async (req, res) => {
//   try {
//     const { image_base64 } = req.body;
//     if (!image_base64) return res.status(400).json({ success: false, message: "No image data" });

//     const metrics = await pythonService.getFrameMetrics(image_base64);
    
//     return res.json({ success: true, metrics });
//   } catch (err) {
//     return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });
//   }
// };

// /**
//  * 5. List Sessions (History)
//  */
// exports.listSessions = async (req, res) => {
//   try {
//     const sessions = await Interview.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: sessions });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };





// // src/controllers/interviewController.js
// const Interview = require("../models/Interview");
// const pythonService = require("../services/pythonService");

// /**
//  * 1. Start a New Interview Session
//  */
// exports.startSession = async (req, res) => {
//   try {
//     const { role, level } = req.body;
//     const sessionId = Date.now().toString();

//     console.log(`🚀 Starting session for ${role} (${level})...`);

//     // 1. Call Python Service
//     const q = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");

//     // 🛡️ Check for null response
//     if (!q) {
//         console.error("❌ Python Service returned null. Using fallback.");
//         return res.json({
//             success: true,
//             sessionId,
//             question: {
//                 _id: Date.now().toString(),
//                 text: "Could not generate a specific question. Please tell me about your background.", 
//                 followUp: "What is your strongest technical skill?",
//                 difficulty: level || "Mid-Level"
//             }
//         });
//     }

//     return res.json({
//       success: true,
//       sessionId,
//       question: {
//         _id: Date.now().toString(),
//         text: q.question || q.text || "Tell me about yourself.",
//         followUp: q.follow_up || q.followUp || "",
//         difficulty: q.difficulty || level
//       }
//     });

//   } catch (err) {
//     console.error("🔥 Start Session Error:", err);
//     return res.status(500).json({ success: false, message: "Failed to start session" });
//   }
// };
// /**
//  * 2. Get Next Question
//  * Called when user clicks "Next Question"
//  */
// exports.getQuestion = async (req, res) => {
//   try {
//     // ✅ FIX 1: Get sessionId from the frontend request
//     const { role, level, sessionId } = req.body; 
    
//     console.log(`🔄 Fetching Next Question for Session: ${sessionId}`);

//     // ✅ FIX 2: Pass sessionId to the service
//     // This tells the service to hit the '/next-question' endpoint instead of '/start'
//     const response = await pythonService.getInterviewQuestion(
//         role || "Software Engineer", 
//         level || "Mid-Level", 
//         sessionId // <--- THIS WAS MISSING
//     );

//     // 🛡️ Handle null response (prevents crashes)
//     if (!response) {
//         return res.json({
//             success: true,
//             question: {
//                 _id: Date.now().toString(),
//                 text: "Describe a challenging technical problem you solved.",
//                 followUp: "How did you debug it?",
//                 difficulty: level,
//             }
//         });
//     }

//     // Robust Data Unpacking
//     let questionText = response.question || "Could not generate question.";
//     let followUpText = response.follow_up || "";

//     // Handle nested object edge case
//     if (typeof response.question === 'object') {
//         questionText = response.question.question;
//         followUpText = response.question.follow_up;
//     }

//     return res.json({
//       success: true,
//       question: {
//         _id: Date.now().toString(),
//         text: questionText,
//         followUp: followUpText,
//         difficulty: response.difficulty || level,
//       }
//     });

//   } catch (err) {
//     console.error("Get Question Error:", err);
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// };
// /**
//  * 3. Analyze Answer
//  * Process transcript with AI
//  */
// exports.analyze = async (req, res) => {
//   try {
//     const { transcript, question } = req.body;
    
//     if (!transcript) {
//         return res.status(400).json({ success: false, message: "Transcript required" });
//     }

//     const analysis = await pythonService.analyzeInterview(transcript);
    
//     // Optional: Save to DB
//     let session = null;
//     if (req.user) {
//       try {
//           session = await Interview.create({
//             userId: req.user._id,
//             question: question || "Unknown",
//             transcript,
//             analysis: analysis || {}, // Ensure analysis isn't null
//           });
//       } catch (dbErr) {
//           console.warn("⚠️ Failed to save to DB:", dbErr.message);
//       }
//     }

//     return res.json({ 
//         success: true, 
//         data: { analysis: analysis || {}, session } 
//     });

//   } catch (err) {
//     console.error("Analysis Error:", err);
//     return res.status(500).json({ success: false, message: "Analysis failed" });
//   }
// };

// /**
//  * 4. Frame Metrics (Video Analysis)
//  */
// exports.getFrameMetrics = async (req, res) => {
//   try {
//     const { image_base64 } = req.body;
//     if (!image_base64) return res.status(400).json({ success: false, message: "No image data" });

//     const metrics = await pythonService.getFrameMetrics(image_base64);
    
//     return res.json({ success: true, metrics });
//   } catch (err) {
//     return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });
//   }
// };

// /**
//  * 5. List Sessions (History)
//  */
// exports.listSessions = async (req, res) => {
//   try {
//     const sessions = await Interview.find({ userId: req.user._id }).sort({ createdAt: -1 });
//     return res.json({ success: true, data: sessions });
//   } catch (err) {
//     return res.status(500).json({ success: false, message: "Server error" });
//   }
// }





// src/controllers/interviewController.js
const Interview = require("../models/Interview");
const pythonService = require("../services/pythonService");

/**
 * 1. Start a New Interview Session
 */
exports.startSession = async (req, res) => {
  try {
    const { role, level } = req.body;
    const sessionId = Date.now().toString();

    console.log(`🚀 Starting session for ${role} (${level})...`);

    const q = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");

    // Fallback if Python fails
    if (!q) {
        return res.json({
            success: true,
            sessionId,
            question: {
                _id: Date.now().toString(),
                text: "Could not generate specific question. Tell me about your background.",
                followUp: "What is your strongest skill?",
                difficulty: level || "Mid-Level"
            }
        });
    }

    return res.json({
      success: true,
      sessionId,
      question: {
        _id: Date.now().toString(),
        text: q.question || q.text || "Tell me about yourself.",
        followUp: q.follow_up || q.followUp || "",
        difficulty: q.difficulty || level
      }
    });

  } catch (err) {
    console.error("🔥 Start Session Error:", err);
    return res.status(500).json({ success: false, message: "Failed to start session" });
  }
};

/**
 * 2. Get Next Question (Robust Version)
 */
exports.getQuestion = async (req, res) => {
  try {
    const { role, level, sessionId } = req.body; 
    console.log(`🔄 Fetching Next Question for Session: ${sessionId}`);

    const response = await pythonService.getInterviewQuestion(
        role || "Software Engineer", 
        level || "Mid-Level", 
        sessionId 
    );

    const fallbackQ = {
        _id: Date.now().toString(),
        text: "Describe a challenging technical project you worked on recently.",
        followUp: "What were the key trade-offs you made?",
        difficulty: level || "Mid-Level"
    };

    if (!response) {
        return res.json({ success: true, question: fallbackQ });
    }

    let questionText = response.text || response.question || "";
    let followUpText = response.follow_up || response.followUp || "";

    if (typeof response.question === 'object' && response.question !== null) {
        questionText = response.question.text || response.question.question || questionText;
        followUpText = response.question.follow_up || response.question.followUp || followUpText;
    }

    // Force fallback if text is missing or is the error string
    if (!questionText || questionText === "Could not generate question.") {
        questionText = fallbackQ.text;
        followUpText = fallbackQ.followUp;
    }

    return res.json({
      success: true,
      question: {
        _id: Date.now().toString(),
        text: questionText,
        followUp: followUpText,
        difficulty: response.difficulty || level,
      }
    });

  } catch (err) {
    console.error("Get Question Error:", err);
    return res.json({ 
        success: true, 
        question: {
            _id: Date.now().toString(),
            text: "Tell me about your experience working in a team.",
            followUp: "How do you handle conflicts?",
            difficulty: "Behavioral"
        }
    });
  }
};

/**
 * 3. Analyze Answer
 */
exports.analyze = async (req, res) => {
  try {
    const { transcript, question } = req.body;
    
    // Allow empty transcript to pass through with dummy data
    if (!transcript) {
        return res.json({ 
            success: true, 
            data: { 
                analysis: {
                    strengths: ["N/A"],
                    improvements: ["No answer provided"],
                    clarity_score: 0
                }, 
                session: null 
            } 
        });
    }

    const analysis = await pythonService.analyzeInterview(transcript);
    
    // Save to DB (Optional)
    let session = null;
    if (req.user) {
      try {
          session = await Interview.create({
            userId: req.user._id,
            question: question || "Unknown",
            transcript,
            analysis: analysis || {},
          });
      } catch (dbErr) { console.warn("DB Save Error:", dbErr.message); }
    }

    return res.json({ 
        success: true, 
        data: { analysis: analysis || {}, session } 
    });

  } catch (err) {
    console.error("Analysis Error:", err);
    // Return dummy success to prevent frontend crash
    return res.json({ 
        success: true, 
        data: { 
            analysis: { strengths: [], improvements: [], clarity_score: 0 } 
        } 
    });
  }
};

/**
 * 4. Frame Metrics (Visuals)
 */
exports.getFrameMetrics = async (req, res) => {
  try {
    const { image_base64 } = req.body;
    if (!image_base64) return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });

    const metrics = await pythonService.getFrameMetrics(image_base64);
    return res.json({ success: true, metrics });
  } catch (err) {
    return res.json({ success: false, metrics: { emotion: "Neutral", confidence: 0 } });
  }
};

/**
 * 5. List Sessions (History)
 */
exports.listSessions = async (req, res) => {
  try {
    // If no user, return empty list
    if (!req.user) return res.json({ success: true, data: [] });

    const sessions = await Interview.find({ userId: req.user._id }).sort({ createdAt: -1 });
    return res.json({ success: true, data: sessions });
  } catch (err) {
    return res.status(500).json({ success: false, message: "Server error" });
  }
};