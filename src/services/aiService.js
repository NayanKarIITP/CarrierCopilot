// src/services/aiService.js
const { HfInference } = require("@huggingface/inference");
require("dotenv").config();

// Initialize HuggingFace client
const hf = new HfInference(process.env.HF_API_KEY);

module.exports = {
  /**
   * Generate text using HuggingFace (Llama-3.2-1B-Instruct)
   */
  async generateText(prompt) {
    try {
      const response = await hf.textGeneration({
        model: "meta-llama/Llama-3.2-1B-Instruct",
        inputs: prompt,
        parameters: {
          max_new_tokens: 300,
          temperature: 0.7,
        },
      });

      return response.generated_text;
    } catch (err) {
      console.error("❌ HF Error:", err);
      throw new Error("HuggingFace LLM failed");
    }
  },

  /**
   * Create text embeddings
   */
  async getEmbeddings(text) {
    try {
      const response = await hf.featureExtraction({
        model: "sentence-transformers/all-mpnet-base-v2",
        inputs: text,
      });

      return response;
    } catch (err) {
      console.error("Embedding Error:", err);
      throw new Error("Failed to generate embeddings");
    }
  }
};
