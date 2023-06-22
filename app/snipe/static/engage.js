function recordClick(id) {
    fetch(`/click/${id}/`)
      .then(response => {
        if (response.ok) {
          // Update the click count in the UI
          const engagementElement = document.getElementById(`engagement-${id}`);
          const clickCount = parseInt(engagementElement.innerText);
          engagementElement.innerText = clickCount + 1;
  
          // Fetch the country information for the click
          fetch(`/country/${id}`)
            .then(response => response.json())
            .then(data => {
              const countryName = data.countryName;
              const countryCode = data.countryCode;
  
              // Update the country list for the click
              const countryListContainer = document.getElementById("country-list");
              const countryItem = document.createElement("li");
              countryItem.textContent = `${countryName} (${countryCode})`;
              countryListContainer.appendChild(countryItem);
            })
            .catch(error => console.error('Error:', error));
        }
      })
      .catch(error => console.error('Error:', error));
  }
  
  // Attach the click event listener to the URL links
  const urlLinks = document.getElementsByClassName('url-link');
  Array.from(urlLinks).forEach(link => {
    const id = link.id.replace('url_click', '');
    link.addEventListener('click', () => recordClick(id));
  });
  