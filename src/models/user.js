const mongoose = require("mongoose");
const validator = require("validator");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

const userSchema = new mongoose.Schema(
  {
    fullName: {
      type: String,
      required: [true, "Full name is required"],
      trim: true,
    },

    email: {
      type: String,
      required: [true, "Email is required"],
      unique: true,
      lowercase: true,
      trim: true,
      validate: [validator.isEmail, "Invalid email"],
    },

    password: {
      type: String,
      required: function () {
        return !this.googleId; // password not required for Google users
      },
      minlength: 6,
    },

    googleId: { type: String, default: null },

    photoURL: {
      type: String,
      default:
        "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp",
    },

    // Dashboard flags
    resumeUploaded: { type: Boolean, default: false },
    roadmapGenerated: { type: Boolean, default: false },
    lastLogin: { type: Date, default: Date.now },

    // Resume results saved here
    resumeScore: { type: Number, default: null },
    extractedSkills: { type: [String], default: [] },
    skillGaps: { type: [String], default: [] },

    // Saved roadmap data
    roadmap: { type: Object, default: {} },
  },
  { timestamps: true }
);

// 🔐 HASH PASSWORD
userSchema.pre("save", async function (next) {
  if (!this.isModified("password")) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

// 🔥 CREATE JWT (IMPORTANT — correct payload)
userSchema.methods.getJWT = function () {
  return jwt.sign(
    {
      _id: this._id,     // VERY IMPORTANT — authMiddleware expects `_id`
      email: this.email,
    },
    process.env.JWT_SECRET,
    { expiresIn: "7d" }
  );
};

// Compare passwords
userSchema.methods.validatePassword = async function (input) {
  return bcrypt.compare(input, this.password);
};

module.exports = mongoose.model("User", userSchema);
