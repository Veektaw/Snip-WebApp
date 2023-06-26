const copyButtons = document.querySelectorAll('.copy-btn5');

// Initialize ClipboardJS for each copy button

const copyToClipboard = (text) => {
    navigator.clipboard
      .writeText(text)
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
  
    document.body.appendChild(popup);
  
    setTimeout(() => {
      document.body.removeChild(popup);
    }, 3000);
  };




copyButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    const targetId = event.target.getAttribute('data-clipboard-target');
    const targetElements = document.querySelectorAll(targetId);

    let textToCopy = '';
    targetElements.forEach((element) => {
      textToCopy += element.textContent.trim() + '\n';
    });

    if (textToCopy !== '') {
      navigator.clipboard
        .writeText(textToCopy)
        .then(() => {
          showCopyPopup(textToCopy);
        })
        .catch((error) => {
          console.error('Failed to copy text:', error);
        });
    }
  });
});
