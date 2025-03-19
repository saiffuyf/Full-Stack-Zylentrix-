const express = require("express");
const multer = require("multer");
const Post = require("../models/Post");
const authMiddleware = require("../middleware/authMiddleware");
const fs = require("fs");
const path = require("path");

const router = express.Router();

// Apply authMiddleware first, so req.user is available before multer runs
router.use(authMiddleware);

// Configure Multer (Storage with User-Specific Folder)
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const userId = req.user.id; // Extract user ID from token
        const uploadPath = path.join(__dirname, "../uploads", userId); // Store in user-specific folder

        // Create folder if it doesn't exist
        if (!fs.existsSync(uploadPath)) {
            fs.mkdirSync(uploadPath, { recursive: true });
        }

        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname)); // Unique filename
    }
});

const upload = multer({ storage });

// Get posts for the logged-in user only
router.get("/", async (req, res) => {
    try {
        const posts = await Post.find({ user: req.user.id });

        const updatedPosts = posts.map(post => ({
            ...post._doc,
            image: post.image ? `http://localhost:5000/uploads/${req.user.id}/${post.image}` : null
        }));

        res.json(updatedPosts);
    } catch (error) {
        res.status(500).json({ message: "Error fetching posts" });
    }
});

//Create a post (with image upload)
router.post("/", upload.single("image"), async (req, res) => {
    const { title, content } = req.body;
    const userId = req.user.id; // Get user ID
    const imagePath = req.file ? req.file.filename : null;

    try {
        const post = new Post({ title, content, image: imagePath, user: userId });
        await post.save();
        res.status(201).json(post);
    } catch (error) {
        res.status(500).json({ message: "Error creating post" });
    }
});

// Serve uploaded images
router.use("/uploads", express.static(path.join(__dirname, "../uploads")));

module.exports = router;
