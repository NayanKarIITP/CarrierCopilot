const Trends = require("../models/Trends");
const pythonService = require("../services/pythonService");

exports.getTrends = async (req, res) => {
  try {
    // 1. CLEAR OLD CACHE (Run this once to fix the schema mismatch)
    // We delete any entry that uses the old 'hiringTrends' format
    await Trends.deleteMany({ "hiringTrends": { $exists: true } });

    // 2. FETCH FRESH DATA FROM PYTHON
    console.log(" Connecting to Python for Real-Time 2025 Data...");
    const pythonResult = await pythonService.getMarketTrends();

    // 3. Validation
    if (!pythonResult || !pythonResult.trends || pythonResult.trends.length === 0) {
       console.warn(" Python returned empty trends. Using fallback.");
       throw new Error("Empty data from Python");
    }

    // 4. Save to MongoDB
    // (Optional: We delete all previous records to keep only the latest snapshot)
    await Trends.deleteMany({}); 
    const saved = await Trends.create(pythonResult);
    
    console.log(" Fresh Data Saved & Sent to Frontend");
    return res.json({ success: true, data: saved });

  } catch (err) {
    console.error(" Controller Error:", err.message);

    // 5. EMERGENCY FALLBACK 
    // This ensures charts are NEVER blank, even if Python crashes
    return res.json({
      success: true,
      data: {
        skills: [
          { skill: "Agentic AI (Offline)", demand: 95 },
          { skill: "Rust (Offline)", demand: 88 },
          { skill: "Cybersecurity (Offline)", demand: 85 }
        ],
        // UPDATED KEY: 'trends' (not hiringTrends)
        trends: [
          { month: "Jan", hiring: 100, salaries: 140 },
          { month: "Feb", hiring: 120, salaries: 145 },
          { month: "Mar", hiring: 140, salaries: 150 },
          { month: "Apr", hiring: 130, salaries: 148 },
          { month: "May", hiring: 160, salaries: 155 },
          { month: "Jun", hiring: 180, salaries: 160 }
        ],
        salaries: [
          { role: "Junior Dev", salary: 90 },
          { role: "Senior Dev", salary: 160 }
        ],
        // UPDATED KEYS: snake_case
        insights: {
          growing_market: "N/A (Offline)",
          ai_opportunity: "N/A",
          remote_jobs: "N/A",
          salary_growth: "N/A",
        }
      }
    });
  }
};