(function () {
  function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : "";
  }

  document.addEventListener("DOMContentLoaded", function () {
    const root = document.querySelector(".crm-kanban");
    if (!root) return;

    const moveUrl = root.dataset.moveUrl;
    const csrftoken = getCookie("csrftoken");
    let draggedCard = null;

    root.querySelectorAll(".crm-kanban-card").forEach(function (card) {
      card.addEventListener("dragstart", function (e) {
        draggedCard = card;
        card.classList.add("crm-kanban-card--dragging");
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", card.dataset.dealId);
      });

      card.addEventListener("dragend", function () {
        card.classList.remove("crm-kanban-card--dragging");
        draggedCard = null;
        root.querySelectorAll(".crm-kanban-cards--drag-over").forEach(function (el) {
          el.classList.remove("crm-kanban-cards--drag-over");
        });
      });
    });

    root.querySelectorAll(".crm-kanban-cards").forEach(function (zone) {
      zone.addEventListener("dragover", function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
        zone.classList.add("crm-kanban-cards--drag-over");
      });

      zone.addEventListener("dragleave", function () {
        zone.classList.remove("crm-kanban-cards--drag-over");
      });

      zone.addEventListener("drop", function (e) {
        e.preventDefault();
        zone.classList.remove("crm-kanban-cards--drag-over");
        if (!draggedCard) return;

        const dealId = draggedCard.dataset.dealId;
        const stageId = zone.dataset.stageId;
        const fromStageId = draggedCard.closest(".crm-kanban-cards").dataset.stageId;

        if (fromStageId === stageId) return;

        zone.appendChild(draggedCard);
        updateColumnCounts(root);

        fetch(moveUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({ deal_id: dealId, stage_id: stageId }),
        })
          .then(function (res) {
            return res.json().then(function (data) {
              return { ok: res.ok, data: data };
            });
          })
          .then(function (result) {
            if (!result.ok || !result.data.ok) {
              window.location.reload();
            }
          })
          .catch(function () {
            window.location.reload();
          });
      });
    });
  });

  function updateColumnCounts(root) {
    root.querySelectorAll(".crm-kanban-column").forEach(function (col) {
      const count = col.querySelectorAll(".crm-kanban-card").length;
      const badge = col.querySelector(".crm-kanban-column-count");
      if (badge) badge.textContent = count;
      const empty = col.querySelector(".crm-kanban-column-empty");
      if (empty) empty.style.display = count ? "none" : "block";
    });
  }
})();
