

// src/controllers/interviewController.js
const Interview = require("../models/Interview");
const pythonService = require("../services/pythonService");

// HELPER: Get User ID (Real or Guest)
const getUserId = (req) => {
    if (req.user && req.user._id) return req.user._id;
    // Return a dummy Mongo Object ID for guests/testing
    return "000000000000000000000000"; 
};

// 1. Start Session (Creates DB Record Immediately)

exports.startSession = async (req, res) => {
  try {
    const { role, level } = req.body;
    const sessionId = Date.now().toString();
    const userId = getUserId(req);

    console.log(` Starting session ${sessionId}...`);

    // 1. Try to get AI Question (Safe Mode)
    let q = null;
    let questionText = "Tell me about your background.";
    let followUp = "What is your strongest skill?";

    try {
        // Attempt to get question from Python AI
        q = await pythonService.getInterviewQuestion(role || "Software Engineer", level || "Mid-Level");
        if (q) {
            questionText = q.question || q.text || questionText;
            followUp = q.follow_up || q.followUp || followUp;
        }
    } catch (e) { 
        console.warn("⚠️ AI Start Failed (Quota or Network):", e.message); 
    }

    // 2.  FORCE SAVE TO DB IMMEDIATELY

    try {
        await Interview.create({
            userId: userId,
            sessionId: sessionId,
            role: role || "Software Engineer",
            level: level || "Mid-Level",
            question: questionText,
            transcript: "",
            analysis: {},
        });
        console.log(` Session ${sessionId} INITIALIZED in DB.`);
    } catch (dbErr) {
        console.error(" Database Init Error:", dbErr.message);
    }

    return res.json({
      success: true,
      sessionId,
      question: {
        _id: Date.now().toString(),
        text: questionText,
        followUp: followUp,
        difficulty: level || "Mid-Level"
      }
    });

  } catch (err) {
    console.error(" Start Session Critical Error:", err);
    return res.status(500).json({ success: false, message: "Failed to start" });
  }
};

//  2. Get Next Question
exports.getQuestion = async (req, res) => {
  try {
    const { role, level, sessionId } = req.body; 
    
    // Fallback if AI fails
    const fallbackQ = {
        text: "Describe a challenging technical project you worked on.",
        followUp: "What were the trade-offs?",
        difficulty: level
    };

    let response = null;
    let questionText = fallbackQ.text;
    let followUpText = fallbackQ.followUp;

    try {
        response = await pythonService.getInterviewQuestion(role, level, sessionId);
        if (response) {
            questionText = response.text || response.question || fallbackQ.text;
            followUpText = response.follow_up || response.followUp || fallbackQ.followUp;
        }
    } catch (e) { 
        console.warn(" AI Next-Q Failed (Quota/Network)"); 
    }

    if (questionText.includes("Could not generate")) questionText = fallbackQ.text;

    return res.json({
      success: true,
      question: {
        _id: Date.now().toString(),
        text: questionText,
        followUp: followUpText,
        difficulty: level,
      }
    });
  } catch (err) {
    return res.json({ success: true, question: { text: "Tell me about your teamwork skills.", followUp: "Example?", difficulty: "Behavioral" } });
  }
};

// 3. Analyze Answer 

exports.analyze = async (req, res) => {
  try {
    //  FIX 1: Extract 'sessionId' properly
    const { transcript, question, sessionId } = req.body; 
    const userId = getUserId(req);

    if (!transcript) return res.json({ success: true, data: { analysis: {} } });

    // 1. Try AI Analysis (Isolated Block)
    let analysis = { 
        strengths: ["Good effort"], 
        improvements: ["AI currently unavailable due to high traffic"], 
        clarity_score: 75,
        confidence_estimate: 80
    };

    try {
        const aiResult = await pythonService.analyzeInterview(transcript);
        if (aiResult && Object.keys(aiResult).length > 0) {
            analysis = aiResult;
        }
    } catch (e) {
        console.warn(" AI Analysis Failed (Quota):", e.message);
        // We continue anyway so we can save the user's answer!
    }
    
    // 2.  FORCE SAVE TO DB (Happens even if AI failed)
    let session = null;
    try {
        session = await Interview.create({
            userId: userId,
            sessionId: sessionId || "unknown", 
            question: question || "Unknown",
            transcript,
            analysis: analysis,
        });
        console.log(`📝 Analysis SAVED for Session ${sessionId}`);
    } catch (dbErr) {
        console.error(" Database Save Error:", dbErr.message);
    }

    return res.json({ success: true, data: { analysis, session } });
  } catch (err) {
    console.error(" Analysis Critical Error:", err);
    return res.json({ success: true, data: { analysis: {}, session: null } });
  }
};

// 4. Frame Metrics (Visuals)

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

//  5. List Sessions (History)

exports.listSessions = async (req, res) => {
  try {
    const userId = getUserId(req);
    const sessions = await Interview.find({ userId: userId }).sort({ createdAt: -1 });
    return res.json({ success: true, data: sessions });
  } catch (err) {
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

/**
 * 6. Get Aggregated Session Report
 * Calculates average scores across ALL questions in the session.
 */
exports.getSessionById = async (req, res) => {
  try {
    const { sessionId } = req.params;
    console.log(`🔎 Generating Aggregate Report for Session: ${sessionId}`);

    // 1. Fetch ALL questions for this session ID
    const sessions = await Interview.find({ sessionId }).sort({ createdAt: 1 });

    if (!sessions || sessions.length === 0) {
        return res.json({ success: false, message: "No data found." });
    }

    // 2. Calculate Averages & Merge Feedback
    let totalClarity = 0;
    let totalConfidence = 0;
    let allStrengths = [];
    let allImprovements = [];
    let fillerWordsTotal = {};

    sessions.forEach(s => {
        const ana = s.analysis || {};
        
        // Sum scores
        totalClarity += ana.clarity_score || 0;
        totalConfidence += ana.confidence_estimate || 0;

        // Collect feedback
        if (Array.isArray(ana.strengths)) allStrengths.push(...ana.strengths);
        if (Array.isArray(ana.improvements)) allImprovements.push(...ana.improvements);

        // Sum filler words
        if (ana.filler_words_count) {
            Object.entries(ana.filler_words_count).forEach(([word, count]) => {
                fillerWordsTotal[word] = (fillerWordsTotal[word] || 0) + count;
            });
        }
    });

    // Compute Averages
    const count = sessions.length;
    const avgClarity = Math.round(totalClarity / count);
    const avgConfidence = Math.round(totalConfidence / count);

    // Deduplicate feedback (taking top unique ones)
    const uniqueStrengths = [...new Set(allStrengths)].slice(0, 5);
    const uniqueImprovements = [...new Set(allImprovements)].slice(0, 5);

    // 3. Construct the Aggregated Response
    const aggregatedData = {
        _id: sessions[0]._id, // ID of first doc (for reference)
        sessionId: sessionId,
        role: sessions[0].role,
        level: sessions[0].level,
        createdAt: sessions[0].createdAt,
        
        // Global Stats
        analysis: {
            clarity_score: avgClarity,
            confidence_estimate: avgConfidence,
            strengths: uniqueStrengths,
            improvements: uniqueImprovements,
            filler_words_count: fillerWordsTotal
        },

        // Detailed History (List of all Q&As)
        history: sessions.map((s, index) => ({
            number: index + 1,
            question: s.question,
            transcript: s.transcript,
            score: s.analysis?.clarity_score || 0
        }))
    };

    return res.json({ success: true, data: aggregatedData });

  } catch (err) {
    console.error("Get Session Error:", err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};