const mongoose = require("mongoose");
const PostSchema = new mongoose.Schema({
    title: { type: String },
    content: { type: String },
    image: { type: String },
    user: { type: mongoose.Schema.Types.ObjectId, ref: "User",required:true}
});
module.exports = mongoose.model("Post", PostSchema);
