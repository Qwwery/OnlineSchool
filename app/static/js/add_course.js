(() => {
  const form = document.getElementById("addCourseForm");

  if (!form) {
    console.error("Не найдена форма #addCourseForm");
    return;
  }

  // Защита от повторной инициализации
  if (form.dataset.bindSubmit === "true") {
    return;
  }

  form.dataset.bindSubmit = "true";

  const errorBox = form.querySelector("[data-form-error]");
  const successBox = form.querySelector("[data-form-success]");
  const submitButton = form.querySelector("button[type='submit']");

  form.addEventListener("submit", onSubmit);

  async function onSubmit(event) {
    event.preventDefault();
    event.stopPropagation();

    // Железная защита от двойной отправки
    if (submitButton.disabled) {
      return;
    }

    submitButton.disabled = true;

    hideMessage(errorBox);
    hideMessage(successBox);

    const formData = new FormData(form);

    const payload = {
      title: String(formData.get("title") || "").trim(),
      description: String(formData.get("description") || "").trim(),
      price: Number(formData.get("price") || 0),
      image_path: String(formData.get("image_path") || "").trim() || null,
    };

    try {
      const response = await fetch("/api/course/new", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify(payload),
      });

      const text = await response.text();

      let data = null;

      try {
        data = JSON.parse(text);
      } catch {
        data = null;
      }

      if (!response.ok) {
        throw new Error(getErrorMessage(data, response.status));
      }

      showMessage(successBox, data?.message || "Курс создан");

      form.reset();

      // Если бэк вернул id курса, можно сразу перейти на него
      const newCourseId = data?.course_id || data?.id || data?.course?.id;

      if (newCourseId) {
        setTimeout(() => {
          window.location.href = `/course/${newCourseId}`;
        }, 500);
      }
    } catch (error) {
      console.error("Ошибка создания курса:", error);
      showMessage(errorBox, error.message || "Не удалось создать курс");
    } finally {
      submitButton.disabled = false;
    }
  }

  function showMessage(element, message) {
    if (!element) {
      return;
    }

    element.textContent = message;
    element.hidden = false;
  }

  function hideMessage(element) {
    if (!element) {
      return;
    }

    element.textContent = "";
    element.hidden = true;
  }

  function getErrorMessage(data, status) {
    if (!data) {
      return `Ошибка сервера: ${status}`;
    }

    if (typeof data.detail === "string") {
      return data.detail;
    }

    if (Array.isArray(data.detail)) {
      return data.detail.map((item) => item.msg).join(" ");
    }

    if (data.message) {
      return data.message;
    }

    return `Ошибка: ${status}`;
  }
})();
