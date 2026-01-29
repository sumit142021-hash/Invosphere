

// Wait for DOM to load before running animations
document.addEventListener("DOMContentLoaded", function () {
  // Smooth entrance animation for hero section
  const heroText = document.querySelector(".welcome-text");
  const subText = document.querySelector(".sub-text");
  const buttons = document.querySelectorAll(".btn-start, .btn-admin");

  heroText.classList.add("animate__animated", "animate__fadeInDown");
  subText.classList.add("animate__animated", "animate__fadeInUp");

  buttons.forEach((btn, index) => {
    setTimeout(() => {
      btn.classList.add("animate__animated", "animate__zoomIn");
    }, 300 * index);
  });

  // Scroll animation for food images
  const foodImages = document.querySelectorAll(".food-img");

  const revealOnScroll = () => {
    const triggerBottom = window.innerHeight * 0.8;
    foodImages.forEach((img) => {
      const boxTop = img.getBoundingClientRect().top;
      if (boxTop < triggerBottom) {
        img.classList.add("animate__animated", "animate__bounceIn");
      }
    });
  };

  window.addEventListener("scroll", revealOnScroll);
  revealOnScroll();

  // Button click animation + message
  const startBtn = document.querySelector(".btn-start");
  const adminBtn = document.querySelector(".btn-admin");

  if (startBtn) {
    startBtn.addEventListener("click", () => {
      startBtn.classList.add("clicked");
      setTimeout(() => {
        startBtn.classList.remove("clicked");
        window.location.href = "/menu/"; // example route
      }, 400);
    });
  }

  if (adminBtn) {
    adminBtn.addEventListener("click", () => {
      adminBtn.classList.add("clicked");
      setTimeout(() => {
        adminBtn.classList.remove("clicked");
        window.location.href = "/admin/"; // example route
      }, 400);
    });
  }
});

// Optional hover bounce effect for icons
const icons = document.querySelectorAll(".food-img");
icons.forEach((icon) => {
  icon.addEventListener("mouseover", () => {
    icon.style.transform = "scale(1.2)";
  });
  icon.addEventListener("mouseleave", () => {
    icon.style.transform = "scale(1)";
  });
});


// Bill animation on billing page
document.addEventListener("DOMContentLoaded", function() {
  const bill = document.getElementById('bill-summary');
  if (bill) {
    // Add Animate.css class dynamically
    bill.classList.add('animate__fadeInDown'); // or animate__slideInUp / animate__zoomIn
  }
});


function finalizeAndPrint() {

    const bill = document.getElementById('bill-summary');
    if (!bill) return;

    // 1️⃣ Open print window

            const newWin = window.open('', 'Print-Bill', 'width=600,height=600');
        newWin.document.body.innerHTML = `
            <html>
              <head>
                <title>Bill</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
                <style>body{padding:20px;}</style>
              </head>
              <body>
                ${document.getElementById('bill-summary').outerHTML}
              </body>
            </html>
        `;
        newWin.print();
        newWin.close();

    // 2️⃣ Submit form to clear cart
    document.getElementById('finalizeBillForm').submit();
}


