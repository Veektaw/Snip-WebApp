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


  document.body.appendChild(popup);


  setTimeout(() => {
    document.body.removeChild(popup);
  }, 3000);
};

copyButton.addEventListener("click", (event) => {
  event.preventDefault();
  const textToCopy = shortUrl.textContent;
  copyToClipboard(textToCopy);
});



// const saveCountry = (formData) => {

//   axios.post('/save_country', formData)
//     .then(response => {
//       const { country, clicks } = response.data;
//       // Update UI with the received country and clicks data
//       const countryElement = document.createElement('li');
//       countryElement.textContent = `${country} - Clicks: ${clicks}`;
//       const countryList = document.getElementById('country-list');
//       countryList.appendChild(countryElement);
//     })
//     .catch(error => {
//       console.error('Failed to save country:', error);
//     });
// };


// const handleSubmit = (event) => {
//   event.preventDefault();


//   const form = event.target;
//   const formData = new FormData(form);


//   saveCountry(formData);
// };


// const form = document.getElementById('country-form');
// form.addEventListener('submit', handleSubmit);
