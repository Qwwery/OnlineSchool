document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[data-api-url]");

  if (!form) {
    return;
  }

  const errorBox = form.querySelector("[data-form-error]");
  const successBox = form.querySelector("[data-form-success]");
  const button = form.querySelector("button[type='submit']");

  if (button) {
    button.dataset.defaultText = button.textContent.trim();
  }

  form.addEventListener("submit", onSubmit);

  async function onSubmit(event) {
    event.preventDefault();

    const url = form.dataset.apiUrl;
    const payload = Object.fromEntries(new FormData(form).entries());

    clearMessages();
    setLoading(true);

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(payload),
      });

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        showError(getErrorMessage(data, response.status));
        return;
      }

      showSuccess(getSuccessMessage(url, data));
      form.reset();

      /*
               Если не хочешь редирект, просто убери эти setTimeout.

               Сейчас сделано так:
               после регистрации переходим на страницу входа,
               после входа переходим на главную.
            */

      if (url === "/reg") {
        setTimeout(() => {
          window.location.href = "/log";
        }, 700);
      }

      if (url === "/log") {
        setTimeout(() => {
          window.location.href = "/";
        }, 700);
      }
    } catch {
      showError("Не удалось отправить запрос. Проверь, что сервер запущен.");
    } finally {
      setLoading(false);
    }
  }

  function getErrorMessage(data, status) {
    if (!data) {
      return `Ошибка сервера: ${status}`;
    }

    if (typeof data.detail === "string") {
      return data.detail;
    }

    if (Array.isArray(data.detail)) {
      return data.detail
        .map((item) => {
          const field = (item.loc || [])
            .filter((part) => part !== "body")
            .join(".");

          if (field) {
            return `${field}: ${item.msg}`;
          }

          return item.msg;
        })
        .join(" ");
    }

    if (data.message) {
      return data.message;
    }

    return `Ошибка: ${status}`;
  }

  function getSuccessMessage(url, data) {
    if (data && data.message) {
      return data.message;
    }

    if (url === "/reg") {
      return "Регистрация прошла успешно.";
    }

    if (url === "/log") {
      return "Вход выполнен.";
    }

    return "Запрос выполнен.";
  }

  function showError(message) {
    if (!errorBox) {
      return;
    }

    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function showSuccess(message) {
    if (!successBox) {
      return;
    }

    successBox.textContent = message;
    successBox.hidden = false;
  }

  function clearMessages() {
    if (errorBox) {
      errorBox.textContent = "";
      errorBox.hidden = true;
    }

    if (successBox) {
      successBox.textContent = "";
      successBox.hidden = true;
    }
  }

  function setLoading(isLoading) {
    if (!button) {
      return;
    }

    button.disabled = isLoading;
    button.textContent = isLoading
      ? "Отправка..."
      : button.dataset.defaultText || "Отправить";
  }
});
