const jwt = require("jsonwebtoken");

module.exports = (req, res, next) => {
    let token = req.header("Authorization");

    if (!token) return res.status(401).json({ message: "Access denied" });

    try {
        token = token.replace("Bearer ", "");  // Remove 'Bearer ' prefix
        const verified = jwt.verify(token, process.env.JWT_SECRET);
        req.user = verified; // Attach user to request
        next();
    } catch (err) {
        return res.status(400).json({ message: "Invalid token" });
    }
};
