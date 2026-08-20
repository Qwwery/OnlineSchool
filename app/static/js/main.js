document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[data-api-url]");

  if (!form) {
    return;
  }

  const errorBox = form.querySelector("[data-form-error]");
  const successBox = form.querySelector("[data-form-success]");
  const button = form.querySelector("button[type='submit']");

  // Сохраняем исходный текст кнопки для восстановления
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
          Accept: "application/json", // Пробуем получить JSON от API
        },
        body: JSON.stringify(payload),
      });

      let data = null;

      // Пытаемся распарсить JSON. Если бэкенд вернул HTML (ошибка 500 или редирект), это упадет в catch
      try {
        // Проверяем, что контент действительно JSON, иначе парсить нельзя
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          data = await response.json();
        } else {
          // Если пришел не JSON (например, HTML страница ошибки от FastAPI), пробуем прочитать текст
          const text = await response.text();
          // Простая эвристика: если это не JSON объект, считаем это ошибкой
          throw new Error(text || `Ошибка сервера: ${response.status}`);
        }
      } catch (parseError) {
        // Если не удалось распарсить JSON, значит бэкенд мог сделать редирект на HTML страницу
        // или вернул HTML шаблон ошибки.
        // В классическом подходе (Jinja) мы НЕ должны ловить это здесь,
        // но для UX скажем пользователю, что что-то пошло не так.
        console.warn(
          "Response is not JSON, likely a server-side redirect or HTML template.",
        );
        // Если сервер сделал редирект (302), браузер сам его обработает, но fetch этого не видит.
        // Поэтому мы просто сбрасываем состояние и даем браузеру сделать свое дело.
        setLoading(false);
        return;
      }

      if (!response.ok) {
        showError(getErrorMessage(data, response.status));
        return;
      }

      // Успех
      showSuccess(getSuccessMessage(url, data));
      form.reset();

      // Логика редиректов ТОЛЬКО если API явно сказал идти дальше (или по URL)
      // Если бэкенд делает редирект через HTTP 302, JS его не увидит, сработает браузер.
      // Этот блок нужен, если бэкенд возвращает JSON с инструкцией.

      if (data && data.redirect) {
        setTimeout(() => {
          window.location.href = data.redirect;
        }, 700);
      } else {
        // Фолбэк логика для твоих роутов, если API не возвращает redirect
        if (url.includes("/api/auth/register")) {
          setTimeout(() => (window.location.href = "/login"), 700);
        }
        if (url.includes("/api/auth/login")) {
          setTimeout(() => (window.location.href = "/"), 700);
        }
      }
    } catch (error) {
      console.error(error);
      setLoading(false);
      showError(
        "Не удалось отправить запрос. Проверьте консоль или статус сервера.",
      );
    } finally {
      // Финальное состояние кнопки
      if (button) {
        button.disabled = false;
        button.textContent = button.dataset.defaultText || "Отправить";
      }
    }
  }

  function getErrorMessage(data, status) {
    if (!data) return `Ошибка сервера: ${status}`;

    // Обработка ошибок валидации Pydantic (FastAPI default)
    if (Array.isArray(data.detail)) {
      return data.detail
        .map((item) => {
          const field = (item.loc || []).filter((p) => p !== "body").join(".");
          return field ? `${field}: ${item.msg}` : item.msg;
        })
        .join("; ");
    }

    if (typeof data.detail === "string") return data.detail;
    if (data.message) return data.message;

    return `Ошибка: ${status}`;
  }

  function getSuccessMessage(url, data) {
    if (data && data.message) return data.message;

    if (url.includes("/api/auth/register"))
      return "Регистрация прошла успешно!";
    if (url.includes("/api/auth/login")) return "Вход выполнен!";

    return "Запрос выполнен успешно.";
  }

  function showError(message) {
    if (!errorBox) return;
    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function showSuccess(message) {
    if (!successBox) return;
    successBox.textContent = message;
    successBox.hidden = false;
  }

  function clearMessages() {
    [errorBox, successBox].forEach((el) => {
      if (el) {
        el.textContent = "";
        el.hidden = true;
      }
    });
  }

  function setLoading(isLoading) {
    if (!button) return;
    button.disabled = isLoading;
    button.textContent = isLoading
      ? "Обработка..."
      : button.dataset.defaultText || "Отправить";
  }
});
