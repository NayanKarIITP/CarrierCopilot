// src/services/pythonService.js
const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

const PYTHON_URL =
  process.env.PYTHON_SERVICE_URL || "http://localhost:8000";

module.exports = {
  /**
   * 🔹 Parse Resume TEXT → Python FastAPI
   * Endpoint: POST /parse-resume-text
   */
  async parseResumeText(text, target_role) {
    try {
      const res = await axios.post(`${PYTHON_URL}/parse-resume-text`, {
        text,
        target_role,
      });
      return res.data;
    } catch (err) {
      console.error(
        "❌ Python Resume Parser Error:",
        err.response?.data || err
      );
      throw new Error("Resume parsing failed");
    }
  },

  /**
   * 🔹 Parse Resume FILE → Python FastAPI
   * Endpoint: POST /parse-resume
   */
  async processResume(filePath, target_role) {
    try {
      const form = new FormData();

      form.append("file", fs.createReadStream(filePath));
      form.append("target_role", target_role);

      const res = await axios.post(`${PYTHON_URL}/parse-resume`, form, {
        headers: form.getHeaders(),
      });

      return res.data;
    } catch (err) {
      console.error(
        "❌ Python Resume FILE Error:",
        err.response?.data || err
      );
      throw new Error("Resume file processing failed");
    }
  },

  /**
   * 🔹 Generate Learning Roadmap
   * Endpoint: POST /roadmap
   */
  async generateRoadmap(skills, role) {
    try {
      const res = await axios.post(`${PYTHON_URL}/roadmap`, {
        skills,
        role,
      });
      return res.data;
    } catch (err) {
      console.error(
        "❌ Python Roadmap Error:",
        err.response?.data || err
      );
      throw new Error("Roadmap generation failed");
    }
  },

  /**
   * 🔹 Skill Gap Analyzer
   * Endpoint: POST /skill-gap
   */
  async skillGapAnalyzer(resumeSkills, targetRole) {
    try {
      const res = await axios.post(`${PYTHON_URL}/skill-gap`, {
        resumeSkills,
        targetRole,
      });
      return res.data;
    } catch (err) {
      console.error(
        "❌ Python Skill Gap Error:",
        err.response?.data || err
      );
      throw new Error("Skill gap analysis failed");
    }
  },

  /**
   * 🔹 Interview: Fetch a new question
   */
  async getInterviewQuestion() {
    try {
      const res = await axios.get(`${PYTHON_URL}/interview/question`);
      return res.data;
    } catch (err) {
      console.error(
        "❌ Python Interview Question Error:",
        err.response?.data || err
      );
      throw new Error("Failed to fetch interview question");
    }
  },

  /**
   * 🔹 Interview: Analyze answer
   */
  async analyzeInterview(transcript) {
    try {
      const res = await axios.post(`${PYTHON_URL}/interview`, {
        answer: transcript,
      });
      return res.data.analysis;
    } catch (err) {
      console.error(
        "❌ Python Interview Analysis Error:",
        err.response?.data || err
      );
      throw new Error("Failed to analyze interview");
    }
  },

  /**
   * 🔹 Market Trends
   */
  async getMarketTrends() {
    try {
      const res = await axios.get(`${PYTHON_URL}/market-trends`);
      return res.data;
    } catch (err) {
      console.error(
        "❌ Python Market Trends Error:",
        err.response?.data || err
      );
      throw new Error("Market trends fetch failed");
    }
  },
};
