const mongoose = require("mongoose");

const trendsSchema = new mongoose.Schema(
  {
    skills: [
      {
        skill: String,
        demand: Number,
      }
    ],
    hiringTrends: [
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
    insights: {
      growingMarkets: Number,
      aiMlOpportunities: Number,
      remotePositions: Number,
      avgSalaryGrowth: Number,
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Trends", trendsSchema);
