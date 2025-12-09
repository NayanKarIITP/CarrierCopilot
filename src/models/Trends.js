const mongoose = require("mongoose");

const trendsSchema = new mongoose.Schema(
  {
    skills: [
      {
        skill: String,
        demand: Number,
      }
    ],
    // UPDATED: Renamed from 'hiringTrends' to 'trends' to match Python
    trends: [
      {
        month: String,
        hiring: Number,
        salaries: Number,
      }
    ],
    salaries: [
      {
        role: String,
        salary: Number,
      }
    ],
    // UPDATED: Changed keys to snake_case and types to String (for "+15%")
    insights: {
      growing_market: { type: String, default: "N/A" },
      ai_opportunity: { type: String, default: "N/A" },
      remote_jobs: { type: String, default: "N/A" },
      salary_growth: { type: String, default: "N/A" },
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Trends", trendsSchema);