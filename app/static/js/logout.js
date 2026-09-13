(() => {
  const logoutForm = document.getElementById("logoutForm");

  if (!logoutForm) {
    return;
  }

  // Защита от повторной инициализации
  if (logoutForm.dataset.bindLogout === "true") {
    return;
  }

  logoutForm.dataset.bindLogout = "true";

  logoutForm.addEventListener("submit", onSubmitLogout);

  async function onSubmitLogout(event) {
    event.preventDefault();
    event.stopPropagation();

    const button = logoutForm.querySelector("button[type='submit']");

    // Защита от двойного клика
    if (button.disabled) {
      return;
    }

    button.disabled = true;

    try {
      const response = await fetch("/api/auth/logout", {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
        credentials: "same-origin",
      });

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        throw new Error(data?.message || "Не удалось выйти из аккаунта");
      }

      if (!data || data.ok !== true) {
        throw new Error("Не удалось выйти из аккаунта");
      }

      showLogoutToast();

      setTimeout(() => {
        window.location.href = "/";
      }, 1500);
    } catch (error) {
      console.error("Ошибка выхода из аккаунта:", error);

      alert(error.message || "Не удалось выйти из аккаунта");

      button.disabled = false;
    }
  }

  function showLogoutToast() {
    const toast = document.getElementById("logoutToast");

    if (!toast) {
      return;
    }

    toast.hidden = false;
  }
})();
