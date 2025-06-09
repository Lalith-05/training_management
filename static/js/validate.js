document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('registerForm');
  const passwordInput = form.querySelector('input[name="password"]');
  const confirmPasswordInput = form.querySelector('input[name="confirm_password"]');
  const usernameInput = form.querySelector('input[name="username"]');

  form.addEventListener('submit', function (e) {
    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // Username length
    if (username.length < 8 || username.length > 15) {
      alert("Username must be between 8 and 15 characters.");
      e.preventDefault();
      return;
    }

    // Password strength
    const strongPassword = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    if (!strongPassword.test(password)) {
      alert("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one number.");
      e.preventDefault();
      return;
    }

    // Confirm password match
    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      e.preventDefault();
      return;
    }
  });
});
