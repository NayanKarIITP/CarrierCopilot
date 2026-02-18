

// src/services/aiService.js
const { GoogleGenerativeAI } = require("@google/generative-ai");
require("dotenv").config();

// Initialize Google GenAI client
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

module.exports = {
  /**
   * Generate text using Google GenAI
   * Best for: Chatbots, Interview Questions, Feedback, Summaries
   */
  async generateText(prompt) {
    try {
      const model = genAI.getGenerativeModel({ model: "gemini-flash-latest" });

      const result = await model.generateContent(prompt);
      const response = await result.response;
      
      return response.text();
    } catch (err) {
      console.error(" Gemini Error:", err);
      throw new Error("Gemini LLM failed to generate text");
    }
  },

  /**
   * Create text embeddings
   * Best for: Semantic Search, Resume Matching, Similarity Checks
   */
  async getEmbeddings(text) {
    try {
      // Use the embedding model for vector conversion
      const model = genAI.getGenerativeModel({ model: "text-embedding-004" });

      const result = await model.embedContent(text);
      
      return result.embedding.values;
    } catch (err) {
      console.error("Embedding Error:", err);
      throw new Error("Failed to generate embeddings");
    }
  }
};