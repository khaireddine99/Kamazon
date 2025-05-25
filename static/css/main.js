// function to scroll back to the top of the screen
document.addEventListener('DOMContentLoaded', function () {
    const backToTop = document.querySelector('.footer-back-to-top');
  
    if (backToTop) {
      backToTop.addEventListener('click', function () {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }
  });


// function to trigger selection when a filter box is checked
document.addEventListener('DOMContentLoaded', function() {
  // get all category checkboxes
  const checkboxes = document.querySelectorAll("input[name='category']")

  // add an event listener to each checkbox 
  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", function() {
      // automatically submit the form when a box is clicked
      document.getElementById("filter-form").submit();
    })
  })
})

// code to uncheck all boxes when button is clicked
document.addEventListener('DOMContentLoaded', function () {
  const clearButton = document.getElementById('clear-filters');
  if (clearButton) {
    clearButton.addEventListener('click', function () {
      const checkboxes = document.querySelectorAll('#filter-form input[type="checkbox"]');
      checkboxes.forEach(cb => cb.checked = false);
      document.getElementById('filter-form').submit();
    });
  }
});

  