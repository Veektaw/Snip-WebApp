const input = document.querySelector("#input-field");
const shortUrl = document.querySelector("#new-url");
const clearButton1 = document.querySelector("#clear-btn");
const clearButton2 = document.querySelector("#clear-btn2");
const copyButton = document.querySelector("#copy-btn[data-clipboard-target='#new-url-label']");
const copyButtons = document.querySelectorAll(".copy-btn2[data-clipboard-target]");
const inputLongUrl = document.querySelector(".text-field-content-row2[name='long_url']");
const inputCustomUrl = document.querySelector(".text-field-content-row2[name='custom_url_entry']");
const customUrlResult = document.querySelector("#new-url-label .new-url-result");

// Clear fields function
const clearFields = () => {
  input.value = '';
  hideResult();
  hideError();
};

const clearFields2 = () => {
  inputLongUrl.value = '';
  inputCustomUrl.value = '';
  hideResult();
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

const showError = () => {
  errorDiv.style.display = "block";
};

const hideError = () => {
  errorDiv.style.display = "none";
};

// Copy button function
copyButton.addEventListener("click", (event) => {
  event.preventDefault();
  const range = document.createRange();
  range.selectNode(customUrlResult);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
});

copyButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.preventDefault();
    const target = button.getAttribute("data-clipboard-target");
    const range = document.createRange();
    const element = document.querySelector(target);
    range.selectNode(element);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand("copy");
    window.getSelection().removeAllRanges();
  });
});
