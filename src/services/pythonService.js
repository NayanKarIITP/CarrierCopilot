
// const axios = require("axios");
// const path = require("path");
// const { spawn } = require("child_process");
// const fs = require("fs");
// const FormData = require("form-data");

// // URL for the Python Microservice (if running separately)
// const PYTHON_URL = process.env.PYTHON_SERVICE_URL || "http://127.0.0.1:8000";

// module.exports = {
//   // --------------------------------------------------
//   // 🔹 1. Process Resume (Fixed & Robust)
//   // --------------------------------------------------
//   async processResume(file, targetRole) {
//     try {
//       const form = new FormData();

//       // Handle file whether it's a path (string) or a Multer object (buffer)
//       if (typeof file === 'string') {
//           if (fs.existsSync(file)) {
//             form.append("file", fs.createReadStream(file));
//           } else {
//             throw new Error(`File not found at path: ${file}`);
//           }
//       } else if (file && file.buffer) {
//           form.append("file", file.buffer, file.originalname || "resume.pdf");
//       } else {
//           // Check if it's a mock/test object or invalid
//           throw new Error("Invalid file format passed to processResume");
//       }

//       form.append("target_role", targetRole || "General");

//       // Send to Python API
//       const res = await axios.post(`${PYTHON_URL}/parse-resume`, form, {
//         headers: { ...form.getHeaders() },
//       });
//       return res.data;

//     } catch (err) {
//       console.error("⚠️ Python API failed or file error:", err.message);

//       // Fallback: Return simulated data so the app doesn't crash during demo/dev
//       return {
//         success: true,
//         score: 72,
//         skills: ["React", "Node.js", "JavaScript (Fallback Analysis)"],
//         missing_skills: ["Python", "Docker"],
//         feedback: "Resume upload simulated. Ensure Python backend is running for real analysis.",
//         extracted_text: "Mock text due to connection failure."
//       };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 2. Roadmap Generator (Uses Local Python Script)
//   // --------------------------------------------------
//   generateRoadmap: (skills, role) => {
//     return new Promise((resolve, reject) => {
//       try {
//         const scriptPath = path.join(__dirname, "../scripts/generate_roadmap.py");
//         const inputData = JSON.stringify({ skills, role });

//         // Ensure python command is correct (python vs python3)
//         const pythonProcess = spawn("python", [scriptPath, inputData]);

//         let dataString = "";
//         let errorString = "";

//         pythonProcess.stdout.on("data", (data) => {
//           dataString += data.toString();
//         });

//         pythonProcess.stderr.on("data", (data) => {
//           errorString += data.toString();
//         });

//         pythonProcess.on("close", (code) => {
//           try {
//             const jsonResult = JSON.parse(dataString);
//             resolve(jsonResult);
//           } catch (err) {
//             console.error("Python Roadmap Error:", errorString || "Invalid JSON output");
//             resolve({ roadmap: [] }); // Return empty on error to prevent crash
//           }
//         });
//       } catch (err) {
//         console.error("Spawn Error:", err);
//         resolve({ roadmap: [] });
//       }
//     });
//   },

//   // --------------------------------------------------
//   // 🔹 3. Interview Question Helper
//   // --------------------------------------------------
//   async getInterviewQuestion(role, level) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/interview/question`, {
//         role: role || "Software Engineer",
//         level: level || "Mid-Level"
//       });
//       return res.data;
//     } catch (err) {
//       return {
//         question: "Describe a challenging project you worked on.",
//         follow_up: "What technical decisions did you make?",
//         difficulty: "Intermediate"
//       };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 4. Skill Gap Analyzer
//   // --------------------------------------------------
//   async skillGapAnalyzer(resumeSkills, targetRole) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/skill-gap`, {
//         current_skills: resumeSkills,
//         target_role: targetRole,
//       });
//       return res.data;
//     } catch (err) {
//       // console.error("❌ Python Skill Gap ERROR:", err.message);
//       return { skillGap: [] };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 5. Analyze Interview Transcript
//   // --------------------------------------------------
//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/interview/analyze`, {
//         transcript: transcript,
//         question: "context"
//       });
//       return res.data;
//     } catch (err) {
//       console.error("❌ Interview Analysis ERROR:", err.message);
//       return {
//         filler_words_count: {},
//         confidence_estimate: 50,
//         strengths: ["Response recorded"],
//         improvements: ["Analysis unavailable"],
//         clarity_score: 0
//       };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 6. Frame Metrics (Video Feed)
//   // --------------------------------------------------
//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/interview/frame-metrics`, {
//         image_base64: imageBase64,
//       });
//       return res.data.metrics;
//     } catch (err) {
//       return { emotion: "Neutral", confidence: 0 };
//     }
//   },
// // --------------------------------------------------
//   // 🔹 7. Market Trends (Fixed Path)
//   // --------------------------------------------------
//   getMarketTrends: () => {
//     return new Promise((resolve) => {
//       // Safety Fallback
//       const safeFallback = {
//         skills: [{ skill: "Backup Data Active", demand: 0 }],
//         trends: [], salaries: [],
//         insights: { growing_market: "Connecting...", ai_opportunity: "...", remote_jobs: "...", salary_growth: "..." }
//       };

//       try {
//         const scriptPath = path.join(__dirname, "../scripts/market_trends.py");

//         // 👇 ENSURE THIS PATH IS CORRECT FOR YOUR PC
//         const pythonExecutable = "C:\\Users\\nkar9\\OneDrive\\Desktop\\Career-Copilot-Backend\\venv\\Scripts\\python.exe";

//         // Debug Log: If you don't see this in your terminal, this file isn't running!
//         console.log("🚀 ATTEMPTING TO SPAWN PYTHON AT:", pythonExecutable);

//         const pythonProcess = spawn(pythonExecutable, [scriptPath], {
//           env: { ...process.env } 
//         });

//         let dataString = "";

//         pythonProcess.stdout.on("data", (data) => {
//           dataString += data.toString();
//         });

//         pythonProcess.stderr.on("data", (data) => {
//           console.error("⚠️ Python Log:", data.toString());
//         });

//         pythonProcess.on("close", (code) => {
//           if (code !== 0) {
//              console.error(`❌ Python crashed (Code ${code})`);
//              resolve(safeFallback); 
//              return;
//           }
//           try {
//             const jsonResult = JSON.parse(dataString);
//             console.log("✅ Python Success! Sending data to frontend.");
//             resolve(jsonResult);
//           } catch (err) {
//             console.error("❌ Invalid JSON received:", dataString);
//             resolve(safeFallback);
//           }
//         });

//       } catch (err) {
//         console.error("❌ Critical Error:", err);
//         resolve(safeFallback);
//       }
//     });
//   },
// };







// //pythonService.js>
// const axios = require("axios");
// const path = require("path");
// const { spawn } = require("child_process");
// const fs = require("fs");
// const FormData = require("form-data");

// // URL for the Python Microservice (if running separately)
// const PYTHON_URL = process.env.PYTHON_SERVICE_URL || "http://127.0.0.1:8000";

// // 👇 CRITICAL: This is the path to your Virtual Environment Python
// // We reuse this variable to ensure ALL scripts run with the correct libraries.
// const PYTHON_EXECUTABLE = "C:\\Users\\nkar9\\OneDrive\\Desktop\\Career-Copilot-Backend\\venv\\Scripts\\python.exe";

// module.exports = {
//   // --------------------------------------------------
//   // 🔹 1. Process Resume (Fixed & Robust)
//   // --------------------------------------------------
//   async processResume(file, targetRole) {
//     try {
//       const form = new FormData();

//       if (typeof file === 'string') {
//           if (fs.existsSync(file)) {
//             form.append("file", fs.createReadStream(file));
//           } else {
//             throw new Error(`File not found at path: ${file}`);
//           }
//       } else if (file && file.buffer) {
//           form.append("file", file.buffer, file.originalname || "resume.pdf");
//       } else {
//           throw new Error("Invalid file format passed to processResume");
//       }

//       form.append("target_role", targetRole || "General");

//       const res = await axios.post(`${PYTHON_URL}/parse-resume`, form, {
//         headers: { ...form.getHeaders() },
//       });
//       return res.data;

//     } catch (err) {
//       console.error("⚠️ Python API failed or file error:", err.message);
//       return {
//         success: true,
//         score: 72,
//         skills: ["React", "Node.js", "JavaScript (Fallback Analysis)"],
//         missing_skills: ["Python", "Docker"],
//         feedback: "Resume upload simulated. Ensure Python backend is running.",
//         extracted_text: "Mock text due to connection failure."
//       };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 2. Roadmap Generator (AI-Powered)
//   // --------------------------------------------------
//   generateRoadmap: (skills, role) => {
//     return new Promise((resolve, reject) => {
//       try {
//         const scriptPath = path.join(__dirname, "../scripts/generate_roadmap.py");
//         const inputData = JSON.stringify({ skills, role });

//         console.log(`🚀 Spawning Roadmap AI for role: ${role}`);

//         // Use the specific VENV python executable
//         const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath], {
//            env: { ...process.env } // Pass API keys
//         });

//         // Write input data to the script's stdin
//         pythonProcess.stdin.write(inputData);
//         pythonProcess.stdin.end();

//         let dataString = "";
//         let errorString = "";

//         pythonProcess.stdout.on("data", (data) => {
//           dataString += data.toString();
//         });

//         pythonProcess.stderr.on("data", (data) => {
//           errorString += data.toString();
//         });

//         pythonProcess.on("close", (code) => {
//           if (code !== 0) {
//             console.error(`❌ Roadmap Script Failed (Code ${code}): ${errorString}`);
//             resolve({ roadmap: [], level: "Beginner" }); 
//             return;
//           }
//           try {
//             const jsonResult = JSON.parse(dataString);
//             console.log("✅ Roadmap Generated Successfully");
//             resolve(jsonResult);
//           } catch (err) {
//             console.error("❌ Roadmap JSON Parse Error:", dataString);
//             resolve({ roadmap: [], level: "Beginner" });
//           }
//         });
//       } catch (err) {
//         console.error("❌ Roadmap Spawn Error:", err);
//         resolve({ roadmap: [], level: "Beginner" });
//       }
//     });
//   },

//   // --------------------------------------------------
//   // 🔹 3. Interview Question Helper
//   // --------------------------------------------------
//   async getInterviewQuestion(role, level) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/interview/question`, {
//         role: role || "Software Engineer",
//         level: level || "Mid-Level"
//       });
//       return res.data;
//     } catch (err) {
//       return {
//         question: "Describe a challenging project you worked on.",
//         follow_up: "What technical decisions did you make?",
//         difficulty: "Intermediate"
//       };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 4. Skill Gap Analyzer
//   // --------------------------------------------------
//   async skillGapAnalyzer(resumeSkills, targetRole) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/skill-gap`, {
//         current_skills: resumeSkills,
//         target_role: targetRole,
//       });
//       return res.data;
//     } catch (err) {
//       return { skillGap: [] };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 5. Analyze Interview Transcript
//   // --------------------------------------------------
//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/interview/analyze`, {
//         transcript: transcript,
//         question: "context"
//       });
//       return res.data;
//     } catch (err) {
//       console.error("❌ Interview Analysis ERROR:", err.message);
//       return {
//         filler_words_count: {},
//         confidence_estimate: 50,
//         strengths: ["Response recorded"],
//         improvements: ["Analysis unavailable"],
//         clarity_score: 0
//       };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 6. Frame Metrics (Video Feed)
//   // --------------------------------------------------
//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(`${PYTHON_URL}/interview/frame-metrics`, {
//         image_base64: imageBase64,
//       });
//       return res.data.metrics;
//     } catch (err) {
//       return { emotion: "Neutral", confidence: 0 };
//     }
//   },

//   // --------------------------------------------------
//   // 🔹 7. Market Trends (Fixed Path)
//   // --------------------------------------------------
//   getMarketTrends: () => {
//     return new Promise((resolve) => {
//       const safeFallback = {
//         skills: [{ skill: "Backup Data Active", demand: 0 }],
//         trends: [], salaries: [],
//         insights: { growing_market: "Connecting...", ai_opportunity: "...", remote_jobs: "...", salary_growth: "..." }
//       };

//       try {
//         const scriptPath = path.join(__dirname, "../scripts/market_trends.py");

//         console.log("🚀 ATTEMPTING TO SPAWN PYTHON AT:", PYTHON_EXECUTABLE);

//         const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath], {
//           env: { ...process.env } 
//         });

//         let dataString = "";

//         pythonProcess.stdout.on("data", (data) => {
//           dataString += data.toString();
//         });

//         pythonProcess.stderr.on("data", (data) => {
//           console.error("⚠️ Python Log:", data.toString());
//         });

//         pythonProcess.on("close", (code) => {
//           if (code !== 0) {
//              console.error(`❌ Python crashed (Code ${code})`);
//              resolve(safeFallback); 
//              return;
//           }
//           try {
//             const jsonResult = JSON.parse(dataString);
//             console.log("✅ Python Success! Sending data to frontend.");
//             resolve(jsonResult);
//           } catch (err) {
//             console.error("❌ Invalid JSON received:", dataString);
//             resolve(safeFallback);
//           }
//         });

//       } catch (err) {
//         console.error("❌ Critical Error:", err);
//         resolve(safeFallback);
//       }
//     });
//   },
// };




// const axios = require("axios");
// const path = require("path");
// const { spawn } = require("child_process");
// const fs = require("fs");

// // ⚡ FAST API URL (Must match your running Python server port)
// // This connects Node.js to the running Python 'app.py' for instant responses.
// const PYTHON_API_URL = "http://127.0.0.1:8000";

// // 🐢 SCRIPT PATH (For Resume & Roadmap tasks)
// // ✅ FIX: Use the specific path you confirmed earlier, or "python" as fallback
// const PYTHON_EXECUTABLE = "C:\\Users\\nkar9\\OneDrive\\Desktop\\Career-Copilot-Backend\\venv\\Scripts\\python.exe";

// // ---------------------------------------------------------
// // 🛠️ HELPER: Run Script Safe (Prevents Node Crashes)
// // ---------------------------------------------------------
// const runPythonScript = (scriptName, inputData = null, args = []) => {
//   return new Promise((resolve, reject) => {
//     try {
//       const scriptPath = path.join(__dirname, `../python/${scriptName}`);

//       // 1. Verify Script Exists
//       if (!fs.existsSync(scriptPath)) {
//           console.error(`❌ Script missing: ${scriptPath}`);
//           return resolve(null); 
//       }

//       console.log(`🐢 Spawning Script: ${scriptName}`);

//       const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
//         env: { ...process.env } // Pass API Keys to Python
//       });

//       // 🛡️ CRASH PROTECTION: Catches "Python not found" errors
//       pythonProcess.on('error', (err) => {
//         console.error("❌ Failed to spawn Python (Check PYTHON_EXECUTABLE path):", err.message);
//         resolve(null); // Return null instead of crashing the server
//       });

//       if (inputData) {
//         pythonProcess.stdin.write(JSON.stringify(inputData));
//         pythonProcess.stdin.end();
//       }

//       let dataString = "";

//       // Capture Standard Output (JSON)
//       pythonProcess.stdout.on("data", (data) => dataString += data.toString());

//       // Capture Error Output (Logs)
//       pythonProcess.stderr.on("data", (data) => console.error(`[Python Log]: ${data}`));

//       pythonProcess.on("close", (code) => {
//         if (code !== 0) {
//           console.error(`❌ ${scriptName} exited with code ${code}`);
//           return resolve(null);
//         }
//         try {
//           resolve(JSON.parse(dataString));
//         } catch (err) {
//           console.error(`❌ JSON Parse Error in ${scriptName}`);
//           resolve(null);
//         }
//       });
//     } catch (err) {
//       console.error("Spawn Error:", err);
//       resolve(null);
//     }
//   });
// };

// module.exports = {
//   // ==================================================
//   // 🟢 REAL-TIME INTERVIEW (Uses HTTP API)
//   // ==================================================

//   /**
//    * 1. Smart Question Fetcher
//    * Automatically switches between START and NEXT based on sessionId.
//    */
//   async getInterviewQuestion(role, level, sessionId = null) {
//     try {
//       // Logic: If no ID, Start New. If ID exists, Get Next.
//       let endpoint = "/interview/start";
//       let payload = { role: role || "Software Engineer", level: level || "Mid-Level" };

//       if (sessionId) {
//         endpoint = "/interview/next-question";
//         payload.sessionId = sessionId;
//       }

//       console.log(`🚀 Calling Python API: ${endpoint} (Session: ${sessionId || "New"})`);


//       // Sending request to Python FastAPI (Port 8000)
//       const res = await axios.post(`${PYTHON_API_URL}${endpoint}`, payload);

//       if (res.data && res.data.question) {
//         return res.data.question;
//       }

//       throw new Error("Python backend returned empty question data");

//     } catch (err) {
//       // 🛡️ Error Handling
//       if (err.code === 'ECONNREFUSED') {
//           console.error("🔥 Connection Refused: Is 'python app.py' running on port 8000?");
//       } else {
//           console.error("🔥 Python API Error:", err.message);
//       }
//       return null; // Controller will handle this by showing a fallback question
//     }
//   },

//   /**
//    * 2. Analyze Answer
//    */
//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, { 
//         transcript: transcript 
//       });
//       return res.data.data.analysis;
//     } catch (err) {
//       console.error("⚠️ Analyze Failed:", err.message);
//       return { 
//         strengths: ["Analysis unavailable"], 
//         improvements: ["Check backend connection"], 
//         clarity_score: 0 
//       };
//     }
//   },

//   /**
//    * 3. Video Frame Metrics
//    */
//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(`${PYTHON_API_URL}/interview/frame-metrics`, { 
//         image_base64: imageBase64 
//       });
//       return res.data.metrics;
//     } catch (err) {
//       // Silent fail to avoid log spamming 30x per second
//       return { emotion: "Neutral", confidence: 0 };
//     }
//   },

//   // ==================================================
//   // 🟡 OFFLINE TASKS (Uses Spawn/Scripts)
//   // ==================================================

//   async processResume(file) {
//     let filePath = file.path || file;
//     // Fix for direct string paths or multer objects
//     if (!fs.existsSync(filePath) && file.path) filePath = file.path;

//     // Resume parsing loads heavy NLP libs, so we spawn it as a separate process
//     return runPythonScript("resume_parser.py", null, [filePath]); 
//   },

//   // 🔹 ADDED: Text-based Resume Analysis (Used by resumeRoutes.js)
//   async analyzeResume(text, targetRole) {
//     const fs = require('fs');
//     const os = require('os');
//     const tempFilePath = path.join(os.tmpdir(), `resume_${Date.now()}.txt`);
//     try {
//         fs.writeFileSync(tempFilePath, text);
//         const result = await runPythonScript("resume_parser.py", null, [tempFilePath]);
//         fs.unlinkSync(tempFilePath); // Cleanup
//         return result;
//     } catch (err) {
//         console.error("Text Analysis Error:", err);
//         return { success: false, message: "Analysis failed" };
//     }
//   },

//   async generateRoadmap(skills, role) {
//     return runPythonScript("roadmap_generator.py", { skills, role });
//   },

//   async skillGapAnalyzer(resumeSkills, targetRole) {
//     return runPythonScript("skill_gap_analyzer.py", { current_skills: resumeSkills, target_role: targetRole });
//   },

//   async getMarketTrends() {
//     return runPythonScript("market_trends.py", {});
//   }
// };





// const axios = require("axios");
// const path = require("path");
// const { spawn } = require("child_process");
// const fs = require("fs");
// const os = require("os");

// /* ---------------------------------------------------
//    PYTHON CONFIG (CROSS-PLATFORM)
// --------------------------------------------------- */

// // Render / Linux uses `python3`, Windows uses `python`
// const PYTHON_EXECUTABLE =
//   process.platform === "win32" ? "python" : "python3";

// // Python FastAPI (Interview Engine)
// const PYTHON_API_URL =
//   process.env.PYTHON_API_URL || "http://127.0.0.1:8000";

// /* ---------------------------------------------------
//    SAFE PYTHON RUNNER
// --------------------------------------------------- */

// const runPythonScript = (scriptName, inputData = null, args = []) => {
//   return new Promise((resolve) => {
//     const scriptPath = path.join(__dirname, `../python/${scriptName}`);

//     if (!fs.existsSync(scriptPath)) {
//       console.error(`❌ Python script not found: ${scriptPath}`);
//       return resolve({ success: false, error: "Script missing" });
//     }

//     const py = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
//       env: process.env,
//     });

//     let stdout = "";
//     let stderr = "";

//     if (inputData) {
//       py.stdin.write(JSON.stringify(inputData));
//       py.stdin.end();
//     }

//     py.stdout.on("data", (data) => (stdout += data.toString()));
//     py.stderr.on("data", (data) => (stderr += data.toString()));

//     py.on("close", (code) => {
//       if (code !== 0) {
//         console.error(`❌ Python error (${scriptName}):`, stderr);
//         return resolve({ success: false, error: stderr });
//       }

//       try {
//         const parsed = JSON.parse(stdout);
//         resolve(parsed);
//       } catch (err) {
//         console.error("❌ Invalid JSON from Python:", stdout);
//         resolve({ success: false, error: "Invalid JSON" });
//       }
//     });

//     py.on("error", (err) => {
//       console.error("❌ Python spawn failed:", err.message);
//       resolve({ success: false, error: err.message });
//     });
//   });
// };

// /* ---------------------------------------------------
//    EXPORT SERVICES
// --------------------------------------------------- */

// module.exports = {
//   /* ---------- INTERVIEW (FASTAPI) ---------- */

//   async getInterviewQuestion(role, level, sessionId = null) {
//     try {
//       const endpoint = sessionId
//         ? "/interview/next-question"
//         : "/interview/start";

//       const payload = sessionId
//         ? { sessionId, role, level }
//         : { role, level };

//       const res = await axios.post(`${PYTHON_API_URL}${endpoint}`, payload);
//       return res.data?.question || null;
//     } catch (err) {
//       console.error("Interview API error:", err.message);
//       return null;
//     }
//   },

//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(
//         `${PYTHON_API_URL}/interview/analyze`,
//         { transcript }
//       );
//       return res.data?.data?.analysis || null;
//     } catch {
//       return {
//         strengths: [],
//         improvements: ["Analysis unavailable"],
//         clarity_score: 0,
//       };
//     }
//   },

//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(
//         `${PYTHON_API_URL}/interview/frame-metrics`,
//         { image_base64: imageBase64 }
//       );
//       return res.data?.metrics || {};
//     } catch {
//       return {};
//     }
//   },

//   /* ---------- OFFLINE AI (SPAWN) ---------- */

//   async processResume(filePath) {
//     return runPythonScript("resume_parser.py", null, [filePath]);
//   },

//   async analyzeResume(text) {
//     const tempFile = path.join(os.tmpdir(), `resume_${Date.now()}.txt`);
//     fs.writeFileSync(tempFile, text);
//     const result = await runPythonScript("resume_parser.py", null, [tempFile]);
//     fs.unlinkSync(tempFile);
//     return result;
//   },

//   async generateRoadmap(skills, role) {
//     return runPythonScript("roadmap_generator.py", { skills, role });
//   },

//   async skillGapAnalyzer(resumeSkills, targetRole) {
//     return runPythonScript("skill_gap_analyzer.py", {
//       current_skills: resumeSkills,
//       target_role: targetRole,
//     });
//   },

//   async getMarketTrends() {
//     return runPythonScript("market_trends.py", {});
//   },
// };






// const axios = require("axios");
// const fs = require("fs");
// const FormData = require("form-data");

// /* ---------------------------------------------------
//    PYTHON SERVICE CONFIG (PRODUCTION SAFE)
// --------------------------------------------------- */

// // 🔥 MUST be public Render URL of Python service
// const PYTHON_SERVICE_URL =
//   process.env.PYTHON_SERVICE_URL ||
//   "https://carriercopilot.onrender.com"; // change if name differs

// /* ---------------------------------------------------
//    EXPORT SERVICES
// --------------------------------------------------- */

// module.exports = {
//   /* =====================================================
//      RESUME ANALYSIS
//   ===================================================== */

//   async processResume(filePath, targetRole = "fullstack-developer") {
//     try {
//       const formData = new FormData();
//       formData.append("file", fs.createReadStream(filePath));
//       formData.append("target_role", targetRole);

//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}/resume/analyze`,
//         formData,
//         {
//           headers: formData.getHeaders(),
//           timeout: 120000, // heavy NLP
//         }
//       );

//       return res.data;
//     } catch (err) {
//       console.error(
//         "❌ Python Resume API Error:",
//         err.response?.data || err.message
//       );
//       return null;
//     }
//   },

//   async analyzeResume(text, targetRole = "fullstack-developer") {
//     try {
//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}/resume/analyze-text`,
//         { text, target_role: targetRole },
//         { timeout: 60000 }
//       );

//       return res.data;
//     } catch (err) {
//       console.error(
//         "❌ Python Text Resume Error:",
//         err.response?.data || err.message
//       );
//       return null;
//     }
//   },

//   /* =====================================================
//      ROADMAP
//   ===================================================== */

//   async generateRoadmap(skills, role) {
//     try {
//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}/roadmap/generate`,
//         { skills, role },
//         { timeout: 60000 }
//       );

//       return res.data;
//     } catch (err) {
//       console.error(
//         "❌ Python Roadmap Error:",
//         err.response?.data || err.message
//       );
//       return null;
//     }
//   },

//   /* =====================================================
//      SKILL GAP
//   ===================================================== */

//   async skillGapAnalyzer(resumeSkills, targetRole) {
//     try {
//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}/skill-gap/analyze`,
//         {
//           current_skills: resumeSkills,
//           target_role: targetRole,
//         }
//       );

//       return res.data;
//     } catch (err) {
//       console.error(
//         "❌ Python Skill Gap Error:",
//         err.response?.data || err.message
//       );
//       return null;
//     }
//   },

//   /* =====================================================
//      INTERVIEW (FASTAPI)
//   ===================================================== */

//   async getInterviewQuestion(role, level, sessionId = null) {
//     try {
//       const endpoint = sessionId
//         ? "/interview/next-question"
//         : "/interview/start";

//       const payload = sessionId
//         ? { sessionId, role, level }
//         : { role, level };

//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}${endpoint}`,
//         payload
//       );

//       return res.data?.question || null;
//     } catch (err) {
//       console.error("❌ Interview API Error:", err.message);
//       return null;
//     }
//   },

//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}/interview/analyze`,
//         { transcript }
//       );

//       return res.data?.data?.analysis || null;
//     } catch {
//       return {
//         strengths: [],
//         improvements: ["Analysis unavailable"],
//         clarity_score: 0,
//       };
//     }
//   },

//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(
//         `${PYTHON_SERVICE_URL}/interview/frame-metrics`,
//         { image_base64: imageBase64 }
//       );

//       return res.data?.metrics || {};
//     } catch {
//       return {};
//     }
//   },
// };





// // src/services/pythonService.js(last working on production)

// const { spawn } = require("child_process");
// const path = require("path");
// const fs = require("fs");
// const os = require("os");

// /* ---------------------------------------------------
//    CONFIG
// --------------------------------------------------- */

// // Windows → python | Linux/Render → python3
// const PYTHON_EXECUTABLE =
//   process.platform === "win32" ? "python" : "python3";

// // Python scripts folder
// const PYTHON_DIR = path.join(__dirname, "../python");

// /* ---------------------------------------------------
//    CORE PYTHON RUNNER (BULLETPROOF)
// --------------------------------------------------- */

// function runPythonScript(scriptName, args = []) {
//   return new Promise((resolve, reject) => {
//     const scriptPath = path.join(PYTHON_DIR, scriptName);

//     if (!fs.existsSync(scriptPath)) {
//       return reject(
//         new Error(`❌ Python script not found: ${scriptName}`)
//       );
//     }

//     const py = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
//       env: process.env,
//     });

//     let stdout = "";
//     let stderr = "";

//     py.stdout.on("data", (data) => {
//       stdout += data.toString();
//     });

//     py.stderr.on("data", (data) => {
//       stderr += data.toString();
//     });

//     py.on("error", (err) => {
//       reject(err);
//     });

//     py.on("close", () => {
//       if (stderr.trim()) {
//         console.warn("⚠️ PYTHON STDERR:\n", stderr);
//       }

//       if (!stdout || !stdout.trim()) {
//         return reject(
//           new Error("❌ Python returned empty output")
//         );
//       }

//       // 🔥 SAFE JSON EXTRACTION (NO REGEX)
//       const jsonStart = stdout.indexOf("{");
//       const jsonEnd = stdout.lastIndexOf("}");

//       if (jsonStart === -1 || jsonEnd === -1) {
//         console.error("❌ RAW PYTHON OUTPUT:\n", stdout);
//         return reject(
//           new Error("❌ No JSON found in Python output")
//         );
//       }

//       const jsonString = stdout.slice(jsonStart, jsonEnd + 1);

//       try {
//         const parsed = JSON.parse(jsonString);
//         resolve(parsed);
//       } catch (err) {
//         console.error("❌ JSON PARSE FAILED:\n", jsonString);
//         reject(err);
//       }
//     });
//   });
// }

// /* ---------------------------------------------------
//    EXPORT SERVICES
// --------------------------------------------------- */

// module.exports = {
//   /* ================= RESUME ================= */

//   async processResume(filePath) {
//     return runPythonScript("resume_parser.py", [filePath]);
//   },

//   async analyzeResume(text, target_role = null) {
//     const tempFile = path.join(os.tmpdir(), `resume_${Date.now()}.txt`);
//     fs.writeFileSync(tempFile, text);

//     try {
//       return await runPythonScript("resume_parser.py", [
//         tempFile,
//         target_role || "",
//       ]);
//     } finally {
//       if (fs.existsSync(tempFile)) {
//         fs.unlinkSync(tempFile);
//       }
//     }
//   },

//   /* ================= ROADMAP ================= */

//   async generateRoadmap(skills, role) {
//     return runPythonScript("roadmap_generator.py", [
//       JSON.stringify({ skills, role }),
//     ]);
//   },

//   async skillGapAnalyzer(resumeSkills, targetRole) {
//     return runPythonScript("skill_gap_analyzer.py", [
//       JSON.stringify({
//         current_skills: resumeSkills,
//         target_role: targetRole,
//       }),
//     ]);
//   },

//   async getMarketTrends() {
//     return runPythonScript("market_trends.py");
//   },

//   /* ================= INTERVIEW ================= */

//   async getInterviewQuestion(role, level, sessionId = null) {
//     return runPythonScript("interview_assistant.py", [
//       JSON.stringify({
//         action: "question",
//         role,
//         level,
//         sessionId,
//       }),
//     ]);
//   },

//   async analyzeInterview(transcript, question = "") {
//     return runPythonScript("interview_assistant.py", [
//       JSON.stringify({
//         action: "analyze",
//         transcript,
//         question,
//       }),
//     ]);
//   },
// };







const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");
const axios = require("axios");

/* ---------------------------------------------------
   CONFIG
--------------------------------------------------- */

// Windows → python | Linux/Render → python3
const PYTHON_EXECUTABLE =
  process.platform === "win32" ? "python" : "python3";

// Python scripts folder
const PYTHON_DIR = path.join(__dirname, "../python");

// Python FastAPI server (INTERVIEW ENGINE)
const PYTHON_API_URL =
  process.env.PYTHON_API_URL || "https://carriercopilot.onrender.com";


/* ---------------------------------------------------
   CORE PYTHON RUNNER (SPAWN)
--------------------------------------------------- */

function runPythonScript(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(PYTHON_DIR, scriptName);

    if (!fs.existsSync(scriptPath)) {
      return reject(new Error(`Python script not found: ${scriptName}`));
    }

    const py = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
      env: process.env,
    });

    let stdout = "";
    let stderr = "";

    py.stdout.on("data", (d) => (stdout += d.toString()));
    py.stderr.on("data", (d) => (stderr += d.toString()));

    py.on("error", reject);

    py.on("close", () => {
      // Log stderr but DON'T fail if stdout is valid
      if (stderr.trim()) {
        console.warn("PYTHON STDERR:", stderr);
      }

      if (!stdout.trim()) {
        return reject(new Error("Python returned no JSON output"));
      }

      const start = stdout.indexOf("{");
      const end = stdout.lastIndexOf("}");

      if (start === -1 || end === -1) {
        console.error("RAW PYTHON OUTPUT:", stdout);
        return reject(new Error("JSON not found in Python output"));
      }

      try {
        const parsed = JSON.parse(stdout.slice(start, end + 1));
        return resolve(parsed);
      } catch (err) {
        console.error("JSON PARSE FAILED:", stdout);
        return reject(err);
      }
    });
    ;
  });
}


/* ---------------------------------------------------
   RESUME (SPAWN BASED)
--------------------------------------------------- */

async function processResume(filePath) {
  return runPythonScript("resume_parser.py", [filePath]);
}

async function analyzeResume(text, targetRole = null) {
  const temp = path.join(os.tmpdir(), `resume_${Date.now()}.txt`);
  fs.writeFileSync(temp, text);

  try {
    return await runPythonScript("resume_parser.py", [
      temp,
      targetRole || "",
    ]);
  } finally {
    if (fs.existsSync(temp)) fs.unlinkSync(temp);
  }
}


/* ---------------------------------------------------
   ROADMAP / TRENDS
--------------------------------------------------- */

async function generateRoadmap(skills, role) {
  return runPythonScript("roadmap_generator.py", [
    JSON.stringify({ skills, role }),
  ]);
}

async function skillGapAnalyzer(resumeSkills, targetRole) {
  return runPythonScript("skill_gap_analyzer.py", [
    JSON.stringify({
      current_skills: resumeSkills,
      target_role: targetRole,
    }),
  ]);
}

async function getMarketTrends() {
  return runPythonScript("market_trends.py");
}


/* ---------------------------------------------------
   INTERVIEW ENGINE (HTTP API)
--------------------------------------------------- */

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
    console.error("Interview question error:", err.message);
    return null;
  }
}

async function analyzeInterview(transcript) {
  try {
    const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, {
      transcript,
    });

    return res.data?.data?.analysis;
  } catch (err) {
    console.error("Interview analysis error:", err.message);
    return {
      strengths: [],
      improvements: ["Analysis unavailable"],
      clarity_score: 0,
    };
  }
}

async function getFrameMetrics(imageBase64) {
  try {
    const res = await axios.post(
      `${PYTHON_API_URL}/interview/frame-metrics`,
      { image_base64: imageBase64 }
    );

    return res.data?.metrics;
  } catch {
    return { emotion: "Neutral", confidence: 0 };
  }
}


/* ---------------------------------------------------
   EXPORT
--------------------------------------------------- */

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
