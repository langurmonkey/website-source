const path = require("path");

module.exports = {
  fontName: "langur-icons", // Font name
  css: true, // Generate a CSS file
  classNamePrefix: "ln", // Prefix for CSS class names
  website: {
    title: "Langur Icons",
    favicon: "../static/img/icon.png",
    logo: "../static/img/profile/myself2.svg",
    version: "1.0.0",
    meta: {
      description: "Langur icon font",
      keywords: "icons, font, svg"
    }
  }
};
