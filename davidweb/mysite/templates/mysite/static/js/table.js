const rows1 = Array.from(document.querySelectorAll('tr'));

function slideOut(row1) {
  row1.classList.add('slide-out');
}

function slideIn(row1, index) {
  setTimeout(function() {
    row1.classList.remove('slide-out');
  }, (index + 5) * 200);  
}

rows1.forEach(slideOut);

rows1.forEach(slideIn);