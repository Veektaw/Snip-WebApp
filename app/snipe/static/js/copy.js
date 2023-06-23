const shortUrl = document.querySelector(".short-url-history");
const copyButton = document.querySelector("#copy-btn");

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => {
      console.log("Text copied to clipboard:", text);
      showCopyPopup(text);
    })
    .catch((error) => {
      console.error("Failed to copy text:", error);
    });
};

const showCopyPopup = (text) => {
  const popup = document.createElement("div");
  popup.classList.add("copy-popup");
  popup.textContent = "Text copied - " + text;

  // Append the popup to the document body
  document.body.appendChild(popup);

  // Automatically remove the popup after a certain duration (e.g., 3 seconds)
  setTimeout(() => {
    document.body.removeChild(popup);
  }, 3000);
};

copyButton.addEventListener("click", (event) => {
  event.preventDefault();
  const textToCopy = shortUrl.textContent;
  copyToClipboard(textToCopy);
});
