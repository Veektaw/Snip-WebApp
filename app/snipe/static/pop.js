document.getElementById('blink').addEventListener('click', function() {
    var popup = document.createElement('div');
    popup.className = 'popup';
    popup.textContent = 'Sign up or login';
  
    document.body.appendChild(popup);
  
    // Close the pop-up when clicked outside
    window.addEventListener('click', function(event) {
      if (!popup.contains(event.target) && event.target !== document.getElementById('blink')) {
        document.body.removeChild(popup);
      }
    });
  });