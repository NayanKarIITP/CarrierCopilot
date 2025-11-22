const User = require("../models/user");
const bcrypt = require("bcrypt");
const validator = require("validator");

// REGISTER USER
exports.registerUser = async (req, res) => {
  try {
    const { fullName, email, password } = req.body;

    // required fields
    if (!fullName || !email || !password) {
      return res.status(400).json({ message: "All fields are required" });
    }

    // email check
    if (!validator.isEmail(email)) {
      return res.status(400).json({ message: "Invalid email" });
    }

    // check if user exists
    let existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({ message: "Email already registered" });
    }

    // create user
    const user = await User.create({
      fullName,
      email,
      password,
    });

    // generate token
    const token = user.getJWT();

    return res.status(201).json({
      message: "Account created successfully",
      token,
      user: {
        id: user._id,
        fullName: user.fullName,
        email: user.email,
        photoURL: user.photoURL,
      },
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: "Server Error" });
  }
};

// LOGIN USER
exports.loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    // validation
    if (!email || !password) {
      return res.status(400).json({ message: "Email & Password required" });
    }

    // find user
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    // validate password
    const isMatch = await user.validatePassword(password);
    if (!isMatch) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    // generate token
    const token = user.getJWT();

    return res.status(200).json({
      message: "Login successful",
      token,
      user: {
        id: user._id,
        fullName: user.fullName,
        email: user.email,
        photoURL: user.photoURL,
      },
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: "Server Error" });
  }
};

// GOOGLE AUTH
exports.googleAuth = async (req, res) => {
  try {
    const { email, fullName, googleId, photoURL } = req.body;

    if (!googleId) {
      return res.status(400).json({ message: "Google ID missing" });
    }

    let user = await User.findOne({ email });

    // if user doesn't exist → create
    if (!user) {
      user = await User.create({
        fullName,
        email,
        googleId,
        password: null,
        photoURL,
      });
    }

    // generate token
    const token = user.getJWT();

    return res.status(200).json({
      message: "Google Login Successful",
      token,
      user: {
        id: user._id,
        fullName: user.fullName,
        email: user.email,
        photoURL: user.photoURL,
      },
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: "Server Error" });
  }
};

// GET LOGGED-IN USER PROFILE
exports.getUserProfile = async (req, res) => {
  return res.status(200).json(req.user);
};
