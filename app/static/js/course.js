(() => {
  const coursePage = document.getElementById("coursePage");

  if (!coursePage) {
    console.error("Не найден элемент #coursePage");
    return;
  }

  const courseId = coursePage.dataset.courseId;
  const currentUserId = coursePage.dataset.userId || "";

  const elements = {
    loading: document.getElementById("courseLoading"),
    error: document.getElementById("courseError"),
    layout: document.getElementById("courseLayout"),
    courseTitle: document.getElementById("courseTitle"),
    courseDescription: document.getElementById("courseDescription"),
    lessonsList: document.getElementById("lessonsList"),
    noLessons: document.getElementById("noLessons"),
    videoPlayer: document.getElementById("videoPlayer"),
    playerPlaceholder: document.getElementById("playerPlaceholder"),
    currentLessonTitle: document.getElementById("currentLessonTitle"),
    currentLessonDescription: document.getElementById(
      "currentLessonDescription",
    ),
    management: document.getElementById("courseManagement"),
    showUploadFormBtn: document.getElementById("showUploadFormBtn"),
    uploadForm: document.getElementById("uploadVideoForm"),
    cancelUploadBtn: document.getElementById("cancelUploadBtn"),
    uploadStatus: document.getElementById("uploadStatus"),
    buyBlock: document.getElementById("buyBlock"),
    buyCourseBtn: document.getElementById("buyCourseBtn"),
    buyPrice: document.getElementById("buyPrice"),
    paymentModal: document.getElementById("paymentModal"),
    modalCourseTitle: document.getElementById("modalCourseTitle"),
    modalPrice: document.getElementById("modalPrice"),
    paymentError: document.getElementById("paymentError"),
    paymentSuccess: document.getElementById("paymentSuccess"),
    confirmPaymentBtn: document.getElementById("confirmPaymentBtn"),
  };

  let isAuthor = false;

  init();

  async function init() {
    bindManagementEvents();

    try {
      const data = await fetchCourse();
      const course = data.course || null;
      const videos = data.videos || [];

      isAuthor = Boolean(
        currentUserId &&
        course &&
        String(course.author_id) === String(currentUserId),
      );

      renderCourse(course);
      renderManagement();
      bindBuyEvents();
      renderBuyBlock(course);
      renderVideos(videos);
      showLayout();
    } catch (error) {
      console.error("Ошибка загрузки курса:", error);
      showCourseError(error.message || "Не удалось загрузить курс");
    }
  }

  function bindManagementEvents() {
    if (elements.showUploadFormBtn) {
      elements.showUploadFormBtn.addEventListener("click", () => {
        hide(elements.showUploadFormBtn);
        show(elements.uploadForm);
      });
    }

    if (elements.cancelUploadBtn) {
      elements.cancelUploadBtn.addEventListener("click", () => {
        hideUploadForm();
      });
    }

    if (elements.uploadForm) {
      elements.uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await uploadVideo();
      });
    }
  }

  async function fetchCourse() {
    const response = await fetch(`/api/course/${courseId}/see`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      credentials: "same-origin",
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

    if (!data || typeof data !== "object") {
      throw new Error(
        "Сервер вернул некорректный ответ. Проверь /api/course/{course_id}/see.",
      );
    }

    return data;
  }

  function renderCourse(course) {
    if (!course) {
      return;
    }

    if (elements.courseTitle) {
      elements.courseTitle.textContent = course.title || "Курс";
    }

    if (elements.courseDescription) {
      elements.courseDescription.textContent = course.description || "";
    }

    if (elements.currentLessonTitle) {
      elements.currentLessonTitle.textContent = course.title || "Курс";
    }
  }

  function renderManagement() {
    if (!elements.management) {
      return;
    }

    elements.management.hidden = !isAuthor;
  }

  function renderVideos(videos) {
    if (!elements.lessonsList) {
      console.error("Не найден элемент #lessonsList");
      return;
    }

    elements.lessonsList.innerHTML = "";

    if (!videos.length) {
      show(elements.noLessons);
      return;
    }

    hide(elements.noLessons);

    videos.forEach((video, index) => {
      const item = document.createElement("li");
      item.className = "lesson-item";
      item.dataset.videoId = video.id;

      item.innerHTML = `
                <div class="lesson-header">
                    <span class="lesson-number">${index + 1}</span>
                    <span class="lesson-title"></span>
                </div>

                <div class="lesson-actions" hidden>
                    <button
                        type="button"
                        class="btn-delete-video"
                    >
                        Удалить
                    </button>
                </div>

                <div class="lesson-loading" hidden>Загрузка...</div>
            `;

      const title = item.querySelector(".lesson-title");
      title.textContent = video.title || `Урок ${index + 1}`;

      const actions = item.querySelector(".lesson-actions");
      const deleteButton = item.querySelector(".btn-delete-video");

      if (isAuthor) {
        show(actions);
      }

      if (deleteButton) {
        deleteButton.addEventListener("click", (event) => {
          event.stopPropagation();
          deleteVideo(video.id);
        });
      }

      item.addEventListener("click", () => {
        onLessonClick(item, video);
      });

      elements.lessonsList.appendChild(item);
    });
  }

  async function onLessonClick(item, video) {
    const loading = item.querySelector(".lesson-loading");
    const title = item.querySelector(".lesson-title").textContent;

    setActiveLesson(item);
    clearCourseError();
    show(loading);

    try {
      const data = await fetchVideoLink(video.id);

      if (!data.url) {
        throw new Error("Не удалось получить ссылку на видео");
      }

      playVideo(data.url, title);
    } catch (error) {
      console.error("Ошибка загрузки видео:", error);
      showCourseError(error.message);
    } finally {
      hide(loading);
    }
  }

  async function fetchVideoLink(videoId) {
    const response = await fetch(`/api/video/${videoId}/link`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      credentials: "same-origin",
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

    if (!data || typeof data !== "object") {
      throw new Error(
        "Сервер вернул некорректный ответ. Проверь /api/video/{video_id}/link.",
      );
    }

    return data;
  }

  function playVideo(url, title) {
    if (!elements.videoPlayer) {
      console.error("Не найден #videoPlayer");
      return;
    }

    elements.videoPlayer.src = url;
    show(elements.videoPlayer);
    hide(elements.playerPlaceholder);

    if (elements.currentLessonTitle) {
      elements.currentLessonTitle.textContent = title;
    }

    if (elements.currentLessonDescription) {
      elements.currentLessonDescription.textContent = "Воспроизведение";
    }

    elements.videoPlayer.play().catch(() => {
      // Автовоспроизведение может быть заблокировано браузером.
    });
  }

  async function uploadVideo() {
    if (!elements.uploadForm) {
      return;
    }

    const formData = new FormData(elements.uploadForm);
    formData.append("course_id", courseId);

    setUploadFormLoading(true);
    hideUploadStatus();

    try {
      const response = await fetch("/api/video/upload", {
        method: "POST",
        body: formData,
        credentials: "same-origin",
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

      showUploadStatus("Видео загружено.", false);
      elements.uploadForm.reset();

      await reloadCourse();
    } catch (error) {
      console.error("Ошибка загрузки видео:", error);
      showUploadStatus(error.message, true);
    } finally {
      setUploadFormLoading(false);
    }
  }

  async function deleteVideo(videoId) {
    const confirmed = window.confirm("Удалить это видео?");

    if (!confirmed) {
      return;
    }

    try {
      const response = await fetch(`/api/video/${videoId}/delete`, {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
        credentials: "same-origin",
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

      await reloadCourse();
    } catch (error) {
      console.error("Ошибка удаления видео:", error);
      showCourseError(error.message);
    }
  }

  async function reloadCourse() {
    try {
      const data = await fetchCourse();

      renderVideos(data.videos || []);
      hideUploadForm();
    } catch (error) {
      console.error("Ошибка обновления курса:", error);
      showCourseError(error.message);
    }
  }

  function hideUploadForm() {
    if (elements.uploadForm) {
      elements.uploadForm.reset();
      hide(elements.uploadForm);
    }

    show(elements.showUploadFormBtn);
    hideUploadStatus();
  }

  function setUploadFormLoading(isLoading) {
    if (!elements.uploadForm) {
      return;
    }

    const buttons = elements.uploadForm.querySelectorAll("button");

    buttons.forEach((button) => {
      button.disabled = isLoading;
    });
  }

  function showUploadStatus(message, isError) {
    if (!elements.uploadStatus) {
      return;
    }

    elements.uploadStatus.textContent = message;
    show(elements.uploadStatus);

    elements.uploadStatus.classList.remove("success", "error");

    if (isError) {
      elements.uploadStatus.classList.add("error");
    } else {
      elements.uploadStatus.classList.add("success");
    }
  }

  function hideUploadStatus() {
    if (!elements.uploadStatus) {
      return;
    }

    elements.uploadStatus.textContent = "";
    hide(elements.uploadStatus);
    elements.uploadStatus.classList.remove("success", "error");
  }

  function setActiveLesson(activeItem) {
    if (!elements.lessonsList) {
      return;
    }

    const items = elements.lessonsList.querySelectorAll(".lesson-item");

    items.forEach((item) => {
      item.classList.remove("active");
    });

    activeItem.classList.add("active");
  }

  function showLayout() {
    hide(elements.loading);
    hide(elements.error);
    show(elements.layout);
  }

  function showCourseError(message) {
    hide(elements.loading);
    hide(elements.layout);

    if (elements.error) {
      elements.error.textContent = message;
      show(elements.error);
    }
  }

  function clearCourseError() {
    if (elements.error) {
      elements.error.textContent = "";
      hide(elements.error);
    }
  }

  function show(element) {
    if (element) {
      element.hidden = false;
    }
  }

  function hide(element) {
    if (element) {
      element.hidden = true;
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
      return data.detail.map((item) => item.msg).join(" ");
    }

    if (data.message) {
      return data.message;
    }

    return `Ошибка: ${status}`;
  }
  let currentCourse = null;

  function renderBuyBlock(course) {
    currentCourse = course;
    if (!elements.buyBlock || !course) return;

    // Не показываем, если юзер — автор или уже купил курс
    const alreadyBought = Boolean(course.access);
    if (isAuthor || !alreadyBought) {
      hide(elements.buyBlock);
      return;
    }

    if (elements.buyPrice) {
      elements.buyPrice.textContent = Number(course.price || 0).toLocaleString(
        "ru-RU",
      );
    }
    show(elements.buyBlock);
  }

  function bindBuyEvents() {
    if (elements.buyCourseBtn) {
      elements.buyCourseBtn.addEventListener("click", openPaymentModal);
    }
    if (elements.paymentModal) {
      elements.paymentModal.addEventListener("click", (e) => {
        if (e.target.dataset.close) closePaymentModal();
      });
    }
    document.addEventListener("keydown", (e) => {
      if (
        e.key === "Escape" &&
        elements.paymentModal &&
        !elements.paymentModal.hidden
      ) {
        closePaymentModal();
      }
    });
    if (elements.confirmPaymentBtn) {
      elements.confirmPaymentBtn.addEventListener("click", confirmPayment);
    }
  }

  function openPaymentModal() {
    if (!currentCourse || !elements.paymentModal) return;
    clearPaymentMessages();
    if (elements.modalCourseTitle)
      elements.modalCourseTitle.textContent = currentCourse.title || "";
    if (elements.modalPrice)
      elements.modalPrice.textContent = Number(
        currentCourse.price || 0,
      ).toLocaleString("ru-RU");
    // Сбрасываем на "Счёт"
    const balanceRadio = elements.paymentModal.querySelector(
      'input[value="balance"]',
    );
    if (balanceRadio) balanceRadio.checked = true;
    show(elements.paymentModal);
  }

  function closePaymentModal() {
    if (elements.paymentModal) hide(elements.paymentModal);
    clearPaymentMessages();
  }

  function clearPaymentMessages() {
    if (elements.paymentError) {
      elements.paymentError.textContent = "";
      hide(elements.paymentError);
    }
    if (elements.paymentSuccess) {
      elements.paymentSuccess.textContent = "";
      hide(elements.paymentSuccess);
    }
  }

  function showPaymentError(msg) {
    if (!elements.paymentError) return;
    elements.paymentError.textContent = msg;
    show(elements.paymentError);
    hide(elements.paymentSuccess);
  }

  function showPaymentSuccess(msg) {
    if (!elements.paymentSuccess) return;
    elements.paymentSuccess.textContent = msg;
    show(elements.paymentSuccess);
    hide(elements.paymentError);
  }

  async function confirmPayment() {
    const selected = elements.paymentModal.querySelector(
      'input[name="payment"]:checked',
    );
    const method = selected ? selected.value : "balance";

    elements.confirmPaymentBtn.disabled = true;
    clearPaymentMessages();

    try {
      const res = await fetch(`/api/enroll/course/${courseId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({ payment_method: method }),
      });

      const text = await res.text();
      let data = null;
      try {
        data = JSON.parse(text);
      } catch {
        data = null;
      }

      if (res.status === 402) {
        showPaymentError(
          "Недостаточно средств на счёте. Пополните баланс и попробуйте снова.",
        );
        return;
      }
      if (!res.ok) {
        showPaymentError(getErrorMessage(data, res.status));
        return;
      }
      if (!data || !data.ok) {
        showPaymentError("Оплата не прошла. Попробуйте позже.");
        return;
      }

      showPaymentSuccess("Курс успешно оплачен! Приятного обучения.");
      // Прячем кнопку покупки и даём пользователю увидеть успех
      hide(elements.buyBlock);
      // Через секунду перечитываем курс, чтобы подтянуть is_enrolled=true
      setTimeout(async () => {
        closePaymentModal();
        await reloadCourse();
      }, 900);
    } catch (err) {
      console.error("Ошибка оплаты:", err);
      showPaymentError("Сетевая ошибка. Попробуйте позже.");
    } finally {
      elements.confirmPaymentBtn.disabled = false;
    }
  }
})();
