// const express = require("express");
// const router = express.Router();
// const { getTrends } = require("../controllers/trendController");

// router.get("/", getTrends);

// module.exports = router;


const express = require("express");
const router = express.Router();

const auth = require("../middleware/authMiddleware");
const { getDashboard } = require("../controllers/dashboardController");

router.get("/", auth, getDashboard);

module.exports = router;
