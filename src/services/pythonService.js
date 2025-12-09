
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






const axios = require("axios");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");
const FormData = require("form-data");

// URL for the Python Microservice (if running separately for heavy tasks like video)
const PYTHON_URL = process.env.PYTHON_SERVICE_URL || "http://127.0.0.1:8000";

// 👇 CRITICAL: Path to Virtual Environment Python
const PYTHON_EXECUTABLE = "C:\\Users\\nkar9\\OneDrive\\Desktop\\Career-Copilot-Backend\\venv\\Scripts\\python.exe";

// Helper to spawn python scripts and return JSON
const runPythonScript = (scriptName, inputData = null, args = []) => {
  return new Promise((resolve, reject) => {
    try {
      // ✅ FIX: Changed from '../scripts/' to '../python/' based on your file tree
      const scriptPath = path.join(__dirname, `../python/${scriptName}`);
      console.log(`🚀 Spawning Python: ${scriptName} at ${scriptPath}`);

      if (!fs.existsSync(scriptPath)) {
         console.error(`❌ Script not found at: ${scriptPath}`);
         resolve(null);
         return;
      }

      const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
        env: { ...process.env } // Pass API Keys
      });

      if (inputData) {
        pythonProcess.stdin.write(JSON.stringify(inputData));
        pythonProcess.stdin.end();
      }

      let dataString = "";
      let errorString = "";

      pythonProcess.stdout.on("data", (data) => {
        dataString += data.toString();
      });

      pythonProcess.stderr.on("data", (data) => {
        errorString += data.toString();
      });

      pythonProcess.on("close", (code) => {
        if (code !== 0) {
          console.error(`❌ ${scriptName} Failed (Code ${code}): ${errorString}`);
          resolve(null);
          return;
        }
        try {
          const jsonResult = JSON.parse(dataString);
          console.log(`✅ ${scriptName} Success`);
          resolve(jsonResult);
        } catch (err) {
          console.error(`❌ ${scriptName} JSON Parse Error. Raw output:`, dataString);
          resolve(null);
        }
      });
    } catch (err) {
      console.error(`❌ Critical Spawn Error (${scriptName}):`, err);
      resolve(null);
    }
  });
};

module.exports = {
  // --------------------------------------------------
  // 🔹 1. Process Resume (Direct Spawn)
  // --------------------------------------------------
  async processResume(file, targetRole) {
    try {
      let filePath = "";
      
      if (typeof file === 'string') {
          if (fs.existsSync(file)) filePath = file;
          else throw new Error(`File not found: ${file}`);
      } else if (file && file.path) {
          filePath = file.path;
      } else {
          throw new Error("Invalid file format");
      }

      // ✅ FIX: Correct path to resume_parser.py
      const scriptPath = path.join(__dirname, "../python/resume_parser.py");
      console.log(`🚀 Processing Resume at: ${scriptPath}`);

      return new Promise((resolve) => {
          const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath, filePath], { env: process.env });
          let data = "";
          let errorLog = "";

          pythonProcess.stdout.on("data", d => data += d);
          pythonProcess.stderr.on("data", d => errorLog += d);
          
          pythonProcess.on("close", (code) => {
              if (code !== 0) {
                  console.error("❌ Resume Parser Failed:", errorLog);
                  resolve({ success: false, error: "Parser crashed" });
                  return;
              }
              try {
                  const result = JSON.parse(data);
                  resolve(result);
              } catch (e) {
                  console.error("❌ Resume JSON Error:", data);
                  resolve({ success: false, error: "Failed to parse Python response" });
              }
          });
      });

    } catch (err) {
      console.error("⚠️ Resume Processing Error:", err.message);
      return { success: false, score: 0, feedback: ["System error."], skills: [] };
    }
  },

  // --------------------------------------------------
  // 🔹 2. Roadmap Generator
  // --------------------------------------------------
  async generateRoadmap(skills, role) {
    // ✅ FIX: Ensure file name matches your tree (generate_roadmap.py vs roadmap_generator.py)
    // Your tree shows 'roadmap_generator.py', but previous code used 'generate_roadmap.py'
    // I will try 'roadmap_generator.py' based on the image provided.
    let result = await runPythonScript("roadmap_generator.py", { skills, role });
    
    if (!result) {
        // Fallback check if the other name was used
        result = await runPythonScript("generate_roadmap.py", { skills, role });
    }

    if (!result) return { roadmap: [], level: "Beginner" };
    return result;
  },

  // --------------------------------------------------
  // 🔹 3. Interview Question Helper
  // --------------------------------------------------
  async getInterviewQuestion(role, level) {
    const result = await runPythonScript("interview_assistant.py", { action: "question", role, level });
    
    if (!result) {
        return {
            question: "Describe a challenging project you worked on.",
            follow_up: "What technical decisions did you make?",
            difficulty: level || "Mid-Level"
        };
    }
    return result;
  },

  // --------------------------------------------------
  // 🔹 4. Skill Gap Analyzer
  // --------------------------------------------------
  async skillGapAnalyzer(resumeSkills, targetRole) {
    const result = await runPythonScript("skill_gap_analyzer.py", { current_skills: resumeSkills, target_role: targetRole });
    return result || { skillGap: [] };
  },

  // --------------------------------------------------
  // 🔹 5. Analyze Interview Transcript
  // --------------------------------------------------
  async analyzeInterview(transcript) {
    const result = await runPythonScript("interview_assistant.py", { action: "analyze", transcript });
    
    return result || {
      filler_words_count: {},
      confidence_estimate: 50,
      strengths: ["Analysis unavailable"],
      improvements: ["Check backend logs"],
      clarity_score: 0
    };
  },

  // --------------------------------------------------
  // 🔹 6. Frame Metrics (Video Feed)
  // --------------------------------------------------
  async getFrameMetrics(imageBase64) {
    // Video analysis is heavy; keep using the Python Server (Flask/FastAPI) via HTTP
    try {
      const res = await axios.post(`${PYTHON_URL}/interview/frame-metrics`, {
        image_base64: imageBase64,
      });
      return res.data.metrics;
    } catch (err) {
      return { emotion: "Neutral", confidence: 0 };
    }
  },

  // --------------------------------------------------
  // 🔹 7. Market Trends
  // --------------------------------------------------
  getMarketTrends: () => {
    return new Promise((resolve) => {
      const safeFallback = {
        skills: [{ skill: "Data Unavailable", demand: 0 }],
        trends: [], salaries: [],
        insights: { growing_market: "N/A", ai_opportunity: "N/A", remote_jobs: "N/A", salary_growth: "N/A" }
      };

      try {
        // ✅ FIX: Correct path
        const scriptPath = path.join(__dirname, "../python/market_trends.py");
        console.log("🚀 Spawning Market Trends at:", scriptPath);

        const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath], {
          env: { ...process.env } 
        });
        
        let dataString = "";
        
        pythonProcess.stdout.on("data", (data) => {
          dataString += data.toString();
        });

        pythonProcess.stderr.on("data", (data) => {
          console.error("⚠️ Market Trends Log:", data.toString());
        });

        pythonProcess.on("close", (code) => {
          if (code !== 0) {
             console.error(`❌ Market Trends Crashed (Code ${code})`);
             resolve(safeFallback); 
             return;
          }
          try {
            const jsonResult = JSON.parse(dataString);
            console.log("✅ Market Trends Data Received");
            resolve(jsonResult);
          } catch (err) {
            console.error("❌ Market Trends Invalid JSON:", dataString);
            resolve(safeFallback);
          }
        });

      } catch (err) {
        console.error("❌ Critical Error:", err);
        resolve(safeFallback);
      }
    });
  },
};










// // src/services/pythonService.js(last correct one)
// const axios = require("axios");
// const path = require("path");
// const { spawn } = require("child_process");
// const fs = require("fs");

// // ⚡ FAST API (For Interviews & Video)
// const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://127.0.0.1:8000";

// // 🐢 SCRIPT PATH (For Resume & Roadmap)
// // ⚠️ CHECK THIS PATH: Verify this file exists on your computer
// const PYTHON_EXECUTABLE = process.env.PYTHON_PATH || "C:\\Users\\nkar9\\OneDrive\\Desktop\\Career-Copilot-Backend\\venv\\Scripts\\python.exe";

// // Helper: Run Script (Safe Version)
// const runPythonScript = (scriptName, inputData = null, args = []) => {
//   return new Promise((resolve, reject) => {
//     try {
//       const scriptPath = path.join(__dirname, `../python/${scriptName}`);
      
//       if (!fs.existsSync(scriptPath)) {
//           console.error(`❌ Script missing: ${scriptPath}`);
//           return resolve(null);
//       }

//       console.log(`🐢 Spawning Script: ${scriptName}`);
      
//       const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
//         env: { ...process.env }
//       });

//       // 🛡️ CRASH PROTECTION: This is what fixes "Failed to fetch"
//       pythonProcess.on('error', (err) => {
//         console.error("❌ Failed to start Python process:", err.message);
//         resolve(null); // Return null instead of crashing the server
//       });

//       if (inputData) {
//         pythonProcess.stdin.write(JSON.stringify(inputData));
//         pythonProcess.stdin.end();
//       }

//       let dataString = "";
//       let errorString = "";

//       pythonProcess.stdout.on("data", (data) => dataString += data.toString());
//       pythonProcess.stderr.on("data", (data) => errorString += data.toString());

//       pythonProcess.on("close", (code) => {
//         if (code !== 0) {
//           console.error(`❌ ${scriptName} Failed: ${errorString}`);
//           return resolve(null);
//         }
//         try {
//           resolve(JSON.parse(dataString));
//         } catch (err) {
//           console.error(`❌ JSON Parse Error (${scriptName})`);
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
//   // 🟢 1. INTERVIEW (Try API first, then Script)
//   async getInterviewQuestion(role, level) {
//     try {
//       // 1. Try Fast API
//       const res = await axios.post(`${PYTHON_API_URL}/interview/start`, { 
//         role: role || "Software Engineer", 
//         level: level || "Mid-Level" 
//       });
      
//       if (res.data && res.data.question) {
//         return res.data.question;
//       }
//       throw new Error("No question in API response");

//     } catch (err) {
//       console.warn("⚠️ Python API Failed, switching to script fallback...");
//       // 2. Fallback to Script
//       return runPythonScript("interview_assistant.py", { action: "question", role, level });
//     }
//   },

//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, { 
//         transcript: transcript 
//       });
//       return res.data.data.analysis;
//     } catch (err) {
//       return runPythonScript("interview_assistant.py", { action: "analyze", transcript });
//     }
//   },

//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(`${PYTHON_API_URL}/interview/frame-metrics`, { 
//         image_base64: imageBase64 
//       });
//       return res.data.metrics;
//     } catch (err) {
//       return { emotion: "Neutral", confidence: 0 };
//     }
//   },

//   // 🟡 2. OFFLINE TASKS (Always Script)
//   async processResume(file) {
//     let filePath = file.path || file;
//     if (!fs.existsSync(filePath) && file.path) filePath = file.path;
//     return runPythonScript("resume_parser.py", null, [filePath]); 
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

// // ⚡ FAST API URL
// const PYTHON_API_URL = "http://127.0.0.1:8000";

// // 🐢 SCRIPT PATH - Use "python" if you are not sure of the full path
// const PYTHON_EXECUTABLE = process.env.PYTHON_PATH || "python";

// // Helper: Run Script (Safe Version)
// const runPythonScript = (scriptName, inputData = null, args = []) => {
//   return new Promise((resolve, reject) => {
//     try {
//       const scriptPath = path.join(__dirname, `../python/${scriptName}`);
      
//       // 🛡️ Check if file exists
//       if (!fs.existsSync(scriptPath)) {
//           console.error(`❌ Script missing: ${scriptPath}`);
//           return resolve(null); 
//       }

//       console.log(`🐢 Spawning Script: ${scriptName}`);
      
//       const pythonProcess = spawn(PYTHON_EXECUTABLE, [scriptPath, ...args], {
//         env: { ...process.env }
//       });

//       // 🛡️ CRASH PROTECTION: This prevents "Failed to fetch" errors
//       pythonProcess.on('error', (err) => {
//         console.error("❌ Failed to spawn Python (Check your PYTHON_PATH):", err.message);
//         resolve(null); // Return null so Node stays alive
//       });

//       if (inputData) {
//         pythonProcess.stdin.write(JSON.stringify(inputData));
//         pythonProcess.stdin.end();
//       }

//       let dataString = "";
      
//       pythonProcess.stdout.on("data", (data) => dataString += data.toString());
//       pythonProcess.stderr.on("data", (data) => console.error(`[Python Log]: ${data}`));

//       pythonProcess.on("close", (code) => {
//         if (code !== 0) {
//           console.error(`❌ Script exited with code ${code}`);
//           return resolve(null);
//         }
//         try {
//           resolve(JSON.parse(dataString));
//         } catch (err) {
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
//   // 🟢 1. INTERVIEW (Try API first, then Script)
//   async getInterviewQuestion(role, level) {
//     try {
//       // 1. Try Fast API
//       const res = await axios.post(`${PYTHON_API_URL}/interview/next-question`, { 
//         sessionId: "demo-session", // Temporary ID for stability
//         role: role || "Software Engineer", 
//         level: level || "Mid-Level" 
//       });
      
//       if (res.data && res.data.question) {
//         return res.data.question;
//       }
//       throw new Error("No question in API response");

//     } catch (err) {
//       console.warn("⚠️ Python API Failed (Question), using fallback...");
//       // 2. Fallback to Script
//       return runPythonScript("interview_assistant.py", { action: "question", role, level });
//     }
//   },

//   async analyzeInterview(transcript) {
//     try {
//       const res = await axios.post(`${PYTHON_API_URL}/interview/analyze`, { 
//         transcript: transcript 
//       });
//       return res.data.data.analysis;
//     } catch (err) {
//       console.warn("⚠️ Python API Failed (Analyze), using fallback...");
//       return runPythonScript("interview_assistant.py", { action: "analyze", transcript });
//     }
//   },

//   async getFrameMetrics(imageBase64) {
//     try {
//       const res = await axios.post(`${PYTHON_API_URL}/interview/frame-metrics`, { 
//         image_base64: imageBase64 
//       });
//       return res.data.metrics;
//     } catch (err) {
//       return { emotion: "Neutral", confidence: 0 };
//     }
//   },

//   // 🟡 2. Offline Tasks
//   async processResume(file) { return runPythonScript("resume_parser.py", null, [file.path]); },
//   async generateRoadmap(skills, role) { return runPythonScript("roadmap_generator.py", { skills, role }); },
//   async skillGapAnalyzer(resumeSkills, targetRole) { return runPythonScript("skill_gap_analyzer.py", { current_skills: resumeSkills, target_role: targetRole }); },
//   async getMarketTrends() { return runPythonScript("market_trends.py", {}); }
// };