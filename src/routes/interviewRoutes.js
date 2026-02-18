
// src/routes/interviewRoutes.js
const express = require('express');
const router = express.Router();
const interviewController = require('../controllers/interviewController');

// Middleware to check if controller functions exist 
const checkHandler = (handler, name) => {
    if (typeof handler !== 'function') {
        console.error(` Error: Controller function '${name}' is missing! Check interviewController.js exports.`);
        // Return a dummy function to prevent server crash during startup
        return (req, res) => res.status(500).json({ message: `Endpoint '${name}' not implemented` });
    }
    return handler;
};

// 1. Start Interview
router.post('/start', checkHandler(interviewController.startSession, 'startSession'));

// 2. Get Next Question
router.post('/next-question', checkHandler(interviewController.getQuestion, 'getQuestion'));

// 3. Analyze Answer
router.post('/analyze', checkHandler(interviewController.analyze, 'analyze'));

// 4. Frame Metrics (Visuals)
router.post('/frame-metrics', checkHandler(interviewController.getFrameMetrics, 'getFrameMetrics'));

// 5. Session History (Optional)
router.get('/history', checkHandler(interviewController.listSessions, 'listSessions'));

// This matches: /api/interview/session/:sessionId
router.get('/session/:sessionId', checkHandler(interviewController.getSessionById, 'getSessionById'));

module.exports = router;
