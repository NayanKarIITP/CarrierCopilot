const Trends = require("../models/Trends");
const pythonService = require("../services/pythonService");

exports.getTrends = async (req, res) => {
  try {
    // Try fetching from MongoDB cache (last 24 hours)
    const oneDay = 24 * 60 * 60 * 1000;
    const cached = await Trends.findOne().sort({ createdAt: -1 });

    if (cached && (Date.now() - cached.createdAt.getTime() < oneDay)) {
      return res.json({ success: true, data: cached });
    }

    // Fetch from Python microservice
    const pythonResult = await pythonService.getMarketTrends();

    // Save in DB for caching
    const saved = await Trends.create(pythonResult);

    return res.json({ success: true, data: saved });

  } catch (err) {
    console.error(err);

    // Fallback static data (same as your UI)
    return res.json({
      success: true,
      data: {
        skills: [
          { skill: "React", demand: 95 },
          { skill: "Python", demand: 92 },
          { skill: "Kubernetes", demand: 88 },
          { skill: "GraphQL", demand: 75 },
          { skill: "AWS", demand: 90 },
          { skill: "Node.js", demand: 87 },
        ],
        hiringTrends: [
          { month: "Jan", hiring: 120, salaries: 165 },
          { month: "Feb", hiring: 140, salaries: 168 },
          { month: "Mar", hiring: 165, salaries: 172 },
          { month: "Apr", hiring: 155, salaries: 170 },
          { month: "May", hiring: 180, salaries: 175 },
          { month: "Jun", hiring: 195, salaries: 180 },
        ],
        salaries: [
          { role: "Junior Dev", salary: 85 },
          { role: "Mid-Level", salary: 130 },
          { role: "Senior Dev", salary: 170 },
          { role: "Tech Lead", salary: 200 },
          { role: "Manager", salary: 220 },
        ],
        insights: {
          growingMarkets: 18,
          aiMlOpportunities: 45,
          remotePositions: 62,
          avgSalaryGrowth: 8,
        }
      }
    });
  }
};
