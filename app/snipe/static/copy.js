// Initialize Clipboard.js
const shortUrl = document.querySelector(".short-url-history");
const copyButton = document.querySelector("#copy-btn")


// Add success and error event listeners
const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        console.log("Text copied to clipboard:", text);
      })
      .catch((error) => {
        console.error("Failed to copy text:", error);
      });
  };
  
  copyButton.addEventListener("click", (event) => {
    event.preventDefault();
    const textToCopy = shortUrl.textContent;
    copyToClipboard(textToCopy);
  });