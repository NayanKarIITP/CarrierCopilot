// // src/services/aiService.js
// const { HfInference } = require("@huggingface/inference");
// require("dotenv").config();

// // Initialize HuggingFace client
// const hf = new HfInference(process.env.HF_API_KEY);

// module.exports = {
//   /**
//    * Generate text using HuggingFace (Llama-3.2-1B-Instruct)
//    */
//   async generateText(prompt) {
//     try {
//       const response = await hf.textGeneration({
//         model: "meta-llama/Llama-3.2-1B-Instruct",
//         inputs: prompt,
//         parameters: {
//           max_new_tokens: 300,
//           temperature: 0.7,
//         },
//       });

//       return response.generated_text;
//     } catch (err) {
//       console.error("❌ HF Error:", err);
//       throw new Error("HuggingFace LLM failed");
//     }
//   },

//   /**
//    * Create text embeddings
//    */
//   async getEmbeddings(text) {
//     try {
//       const response = await hf.featureExtraction({
//         model: "sentence-transformers/all-mpnet-base-v2",
//         inputs: text,
//       });

//       return response;
//     } catch (err) {
//       console.error("Embedding Error:", err);
//       throw new Error("Failed to generate embeddings");
//     }
//   }
// };





// src/services/aiService.js
const { GoogleGenerativeAI } = require("@google/generative-ai");
require("dotenv").config();

// Initialize Google GenAI client
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

module.exports = {
  /**
   * Generate text using Google Gemini 1.5 Flash
   * Best for: Chatbots, Interview Questions, Feedback, Summaries
   */
  async generateText(prompt) {
    try {
      // Use the 'gemini-1.5-flash' model for speed and efficiency
      const model = genAI.getGenerativeModel({ model: "gemini-flash-latest" });

      const result = await model.generateContent(prompt);
      const response = await result.response;
      
      return response.text();
    } catch (err) {
      console.error("❌ Gemini Error:", err);
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