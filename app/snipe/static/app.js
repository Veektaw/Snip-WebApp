// Select elements
const input = document.querySelector("#input-field");
const shortUrl = document.querySelector("#new-url-label .new-url-result");
const shortUrlhistory = document.querySelector(".short-url-history");
const clearButton1 = document.querySelector("#clear-btn");
const clearButton2 = document.querySelector("#clear-btn2");
const copyButton1 = document.querySelector("#copy-btn");
const copyButton2 = document.querySelector("#copy-btn1");
const copyButtons = document.querySelectorAll('.copy-btn5');
const inputLongUrl = document.querySelector(".text-field-content-row2[name='long_url']");
const inputCustomUrl = document.querySelector(".text-field-content-row2[name='custom_url_entry']");
const customUrlResult = document.querySelector("#custom-url-created");
const errorDiv = document.querySelector("#error-div");

// Clear fields functions
const clearFields = () => {
  input.value = '';
  hideResult();
  hideError();
};

const clearFields2 = () => {
  inputLongUrl.value = '';
  inputCustomUrl.value = '';
  hideCustomUrlResult();
  hideError();
};

// Event listeners for clear buttons
clearButton1.addEventListener("click", (event) => {
  event.preventDefault();
  clearFields();
});

clearButton2.addEventListener("click", (event) => {
  event.preventDefault();
  clearFields2();
});

// Show/hide result functions
const showResult = () => {
  shortUrl.style.display = "block";
};

const hideResult = () => {
  shortUrl.style.display = "none";
};

const showCustomUrlResult = () => {
  customUrlResult.style.display = "block";
};

const hideCustomUrlResult = () => {
  customUrlResult.style.display = "none";
};

// Show/hide error functions
const showError = () => {
  errorDiv.style.display = "block";
};

const hideError = () => {
  errorDiv.style.display = "none";
};

// Copy to clipboard function
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => {
      console.log("Text copied to clipboard:", text);
    })
    .catch((error) => {
      console.error("Failed to copy text:", error);
    });
};

// Event listener for copy button 1 (short URL)
copyButton1.addEventListener("click", (event) => {
  event.preventDefault();
  const textToCopy = shortUrl.textContent;
  copyToClipboard(textToCopy);
});

// Event listener for copy button 2 (custom URL)
copyButton2.addEventListener("click", (event) => {
  event.preventDefault();
  const textToCopy = customUrlResult.textContent;
  copyToClipboard(textToCopy);
});

// Event listener for copy buttons in each column
copyButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault();
    const targetId = button.getAttribute('data-clipboard-target');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
      const textToCopy = targetElement.textContent.trim();
      copyToClipboard(textToCopy);
    }
  });
});
