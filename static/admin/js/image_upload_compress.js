(function () {
  const MAX_SIDE = 1800;
  const MIN_BYTES = 900 * 1024;
  const QUALITY = 0.78;
  const SUPPORTED_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);

  let submitter = null;

  function setStatus(text) {
    let node = document.getElementById("image-compress-status");
    if (!node) {
      node = document.createElement("div");
      node.id = "image-compress-status";
      node.style.cssText = [
        "position:fixed",
        "right:16px",
        "bottom:16px",
        "z-index:9999",
        "max-width:320px",
        "padding:10px 12px",
        "border-radius:8px",
        "background:#111827",
        "color:#fff",
        "font:13px/1.4 system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif",
        "box-shadow:0 10px 30px rgba(0,0,0,.25)",
      ].join(";");
      document.body.appendChild(node);
    }
    node.textContent = text;
  }

  function clearStatus() {
    document.getElementById("image-compress-status")?.remove();
  }

  function loadImage(file) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => {
        URL.revokeObjectURL(url);
        resolve(img);
      };
      img.onerror = () => {
        URL.revokeObjectURL(url);
        reject(new Error("Image load failed"));
      };
      img.src = url;
    });
  }

  function canvasToBlob(canvas) {
    return new Promise((resolve) => {
      canvas.toBlob(resolve, "image/webp", QUALITY);
    });
  }

  function targetSize(width, height) {
    const scale = Math.min(1, MAX_SIDE / Math.max(width, height));
    return {
      width: Math.max(1, Math.round(width * scale)),
      height: Math.max(1, Math.round(height * scale)),
    };
  }

  async function compressFile(file) {
    if (!file || file.size < MIN_BYTES || !SUPPORTED_TYPES.has(file.type)) return file;

    const img = await loadImage(file);
    const size = targetSize(img.naturalWidth || img.width, img.naturalHeight || img.height);
    const canvas = document.createElement("canvas");
    canvas.width = size.width;
    canvas.height = size.height;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, size.width, size.height);

    const blob = await canvasToBlob(canvas);
    if (!blob || blob.size >= file.size) return file;

    const name = file.name.replace(/\.[^.]+$/, "") + ".webp";
    return new File([blob], name, {
      type: "image/webp",
      lastModified: Date.now(),
    });
  }

  async function compressInput(input) {
    if (!input.files || !input.files.length) return false;

    const dt = new DataTransfer();
    let changed = false;

    for (const file of input.files) {
      const compressed = await compressFile(file);
      if (compressed !== file) changed = true;
      dt.items.add(compressed);
    }

    if (changed) input.files = dt.files;
    return changed;
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest("button, input[type='submit']");
    if (button && button.form) submitter = button;
  });

  document.addEventListener("submit", async (event) => {
    const form = event.target;
    if (!form || form.dataset.imageUploadCompressed === "1") return;

    const inputs = Array.from(form.querySelectorAll("input[type='file'][accept*='image']"))
      .filter((input) => input.files && input.files.length);
    if (!inputs.length) return;

    event.preventDefault();
    setStatus("Сжимаю изображения перед загрузкой...");

    try {
      let changed = false;
      for (const input of inputs) {
        changed = (await compressInput(input)) || changed;
      }
      form.dataset.imageUploadCompressed = "1";
      setStatus(changed ? "Изображения сжаты, сохраняю..." : "Сохраняю...");
      setTimeout(() => {
        if (form.requestSubmit) {
          form.requestSubmit(submitter && submitter.form === form ? submitter : undefined);
        } else {
          form.submit();
        }
      }, 50);
    } catch (error) {
      clearStatus();
      form.dataset.imageUploadCompressed = "1";
      if (form.requestSubmit) {
        form.requestSubmit(submitter && submitter.form === form ? submitter : undefined);
      } else {
        form.submit();
      }
    }
  }, true);
})();
