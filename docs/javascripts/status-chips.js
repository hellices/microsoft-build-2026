/**
 * Auto-convert status text in tables into colored chips.
 * Runs on every page navigation (Material's instant nav uses document$).
 *
 * Matches the trimmed text content of <td> cells. Keeps original text.
 */
(function () {
  const MAX_LEN = 40;

  function classify(txt) {
    if (txt.length === 0 || txt.length > MAX_LEN) return null;
    if (/private\s+preview/i.test(txt)) return "preview-private";
    if (/public\s+preview/i.test(txt) || /^preview\b/i.test(txt))
      return "preview";
    if (/limited\s+availability/i.test(txt)) return "limited";
    if (/^roadmap\b/i.test(txt)) return "roadmap";
    if (/^event\b/i.test(txt)) return "event";
    if (/^ga\b/i.test(txt)) return "ga";
    return null;
  }

  function apply() {
    document.querySelectorAll(".md-typeset table td").forEach((td) => {
      if (td.querySelector(".status-chip")) return;
      const raw = td.textContent.trim();
      const cls = classify(raw);
      if (!cls) return;
      // Replace the cell's content with a single chip (preserves original text).
      td.innerHTML = `<span class="status-chip status-${cls}">${raw}</span>`;
    });
  }

  // Material with navigation.instant exposes document$ (RxJS subject).
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(apply);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else {
    apply();
  }
})();
