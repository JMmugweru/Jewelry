document.addEventListener("DOMContentLoaded", () => {
  const signinModal = document.getElementById("signinModal");
  const signupModal = document.getElementById("signupModal");
  const previewContainer = document.getElementById("preview");
  const galleryContainer = document.getElementById("gallery");
  const materialBtn = document.getElementById("materialBtn");
  const materialDropdown = document.getElementById("materialDropdown");
  const materialOptions = document.querySelectorAll("[data-material]");
  const generateButton = document.getElementById("generateDesign");

  // Modal Handling
  document
    .getElementById("openSigninModal")
    .addEventListener("click", () => signinModal.classList.remove("hidden"));
  document
    .getElementById("openSignupModal")
    .addEventListener("click", () => signupModal.classList.remove("hidden"));
  document
    .getElementById("closeSigninModal")
    .addEventListener("click", () => signinModal.classList.add("hidden"));
  document
    .getElementById("closeSignupModal")
    .addEventListener("click", () => signupModal.classList.add("hidden"));

  // Material Dropdown Logic
  materialBtn.addEventListener("click", () =>
    materialDropdown.classList.toggle("active")
  );
  materialOptions.forEach((option) => {
    option.addEventListener("click", () => {
      materialBtn.querySelector("span").textContent = option.textContent;
      materialDropdown.classList.remove("active");
    });
  });

  async function checkLogin() {
    const response = await fetch("/check_login");
    const data = await response.json();
    document.body.setAttribute(
      "data-logged-in",
      data.loggedIn ? "true" : "false"
    );
    if (data.loggedIn) loadGallery();
  }
  checkLogin();

  document
    .getElementById("signinForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("signinEmail").value;
      const password = document.getElementById("signinPassword").value;

      try {
        const response = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        alert(data.message || data.error);
        if (data.message) checkLogin();
      } catch (error) {
        alert("Login failed.");
      }
    });

  generateButton.addEventListener("click", async () => {
    if (document.body.getAttribute("data-logged-in") !== "true") {
      alert("Please sign in first!");
      return;
    }

    const prompt =
      document.getElementById("designPrompt").value || "Elegant gold ring";
    const material = materialBtn
      .querySelector("span")
      .textContent.toLowerCase();

    previewContainer.innerHTML = "<p>Generating...</p>";

    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, material }),
    });

    const data = await response.json();
    previewContainer.innerHTML = data.modelUrl
      ? `<iframe src="${data.modelUrl}" class="w-full h-full"></iframe>`
      : "<p>Error generating model.</p>";
    loadGallery();
  });

  async function loadGallery() {
    const response = await fetch("/gallery");
    const data = await response.json();
    galleryContainer.innerHTML = data.error
      ? "<p>No saved designs.</p>"
      : data
          .map(
            (d) =>
              `<div class="gallery-item"><iframe src="${d.modelUrl}" class="w-32 h-32"></iframe><p>${d.prompt} (${d.material})</p></div>`
          )
          .join("");
  }
});
