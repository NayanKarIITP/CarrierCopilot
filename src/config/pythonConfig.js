require("dotenv").config();

module.exports = {
  PYTHON_BASE_URL: process.env.PYTHON_SERVICE_URL || "http://127.0.0.1:5001"
};
