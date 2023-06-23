const input = document.querySelector("#input-field");
const shortUrl = document.querySelector("#new-url-label .new-url-result");
const shortUrlhistory = document.querySelector(".short-url-history");
const clearButton1 = document.querySelector("#clear-btn");
const clearButton2 = document.querySelector("#clear-btn2");
const copyButton1 = document.querySelector("#copy-btn");
const copyButton2 = document.querySelector("#copy-btn1");
const copyButton5 = document.querySelector("#copy-btn5");
const inputLongUrl = document.querySelector(".text-field-content-row2[name='long_url']");
const inputCustomUrl = document.querySelector(".text-field-content-row2[name='custom_url_entry']");
const customUrlResult = document.querySelector("#custom-url-created");
const errorDiv = document.querySelector("#error-div");

// Clear fields function
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

clearButton1.addEventListener("click", (event) => {
  event.preventDefault();
  clearFields();
});

clearButton2.addEventListener("click", (event) => {
  event.preventDefault();
  clearFields2();
});

// Display/hide results and errors functions
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

const showError = () => {
  errorDiv.style.display = "block";
};

const hideError = () => {
  errorDiv.style.display = "none";
};

// Copy button function
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

copyButton1.addEventListener("click", (event) => {
  event.preventDefault();
  const textToCopy = shortUrl.textContent;
  copyToClipboard(textToCopy);
});

copyButton2.addEventListener("click", (event) => {
  event.preventDefault();
  const textToCopy = customUrlResult.textContent;
  copyToClipboard(textToCopy);
});

const handleCopyButtonClick = (event) => {
  event.preventDefault();
  const button = event.target;
  const targetId = button.getAttribute('data-clipboard-target');
  const targetElements = document.querySelectorAll(targetId);

  let textToCopy = "";
  targetElements.forEach((element) => {
    textToCopy += element.textContent + "\n";
  });

  copyToClipboard(textToCopy.trim());
};

const copyButtons = document.querySelectorAll('.copy-btn5');
copyButtons.forEach((button) => {
  button.addEventListener('click', handleCopyButtonClick);
});
