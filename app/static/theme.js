(function () {
  const STYLE_ID = 'medalerts-dark-style';
  if (!document.getElementById(STYLE_ID)) {
    const st = document.createElement('style');
    st.id = STYLE_ID;
    st.textContent = `
      html.dark-mode body { background-color: #0B0F14 !important; color: #E5E7EB !important; }
      html.dark-mode header { background-color: rgba(11, 15, 20, 0.88) !important; border-color: rgba(255,255,255,0.08) !important; }
      html.dark-mode .apple-card, html.dark-mode .bg-white { background-color: #141A22 !important; color: #E5E7EB !important; border-color: rgba(255,255,255,0.08) !important; }
      html.dark-mode .bg-\\[\\#F5F5F7\\], html.dark-mode .bg-\\[\\#F5F5F7\\]\\/80, html.dark-mode .bg-\\[\\#F5F5F7\\]\\/70, html.dark-mode .bg-\\[\\#F5F5F7\\]\\/60 { background-color: #1C2430 !important; color: #E5E7EB !important; }
      html.dark-mode .text-\\[\\#1D1D1F\\] { color: #F3F4F6 !important; }
      html.dark-mode .text-\\[\\#6E6E73\\], html.dark-mode .text-\\[\\#86868B\\], html.dark-mode .text-\\[\\#3A3A3C\\] { color: #9CA3AF !important; }
      html.dark-mode input, html.dark-mode select, html.dark-mode textarea { background-color: #1C2430 !important; color: #F3F4F6 !important; border-color: rgba(255,255,255,0.12) !important; }
      html.dark-mode table thead tr { background-color: #1C2430 !important; }
      html.dark-mode table tbody tr:hover { background-color: rgba(255,255,255,0.04) !important; }
      html.dark-mode .border-black\\/\\[0\\.06\\], html.dark-mode .border-black\\/\\[0\\.05\\], html.dark-mode .border-black\\/10 { border-color: rgba(255,255,255,0.09) !important; }
    `;
    document.head.appendChild(st);
  }

  function applyTheme(dark) {
    document.documentElement.classList.toggle('dark-mode', !!dark);
    const btn = document.getElementById('medThemeToggleBtn');
    if (btn) {
      btn.innerHTML = dark
        ? '<i class="fa-solid fa-sun text-amber-400"></i>'
        : '<i class="fa-solid fa-moon"></i>';
      btn.title = dark ? 'Switch to Day Mode' : 'Night-Duty Dark Mode';
    }
  }

  window.toggleMedTheme = function () {
    const next = !document.documentElement.classList.contains('dark-mode');
    localStorage.setItem('med_theme', next ? 'dark' : 'light');
    applyTheme(next);
  };

  const savedDark = localStorage.getItem('med_theme') === 'dark';
  applyTheme(savedDark);

  document.addEventListener('DOMContentLoaded', () => {
    const hdr = document.querySelector('header > div');
    if (hdr && !document.getElementById('medThemeToggleBtn')) {
      const btn = document.createElement('button');
      btn.id = 'medThemeToggleBtn';
      btn.type = 'button';
      btn.onclick = window.toggleMedTheme;
      btn.className = 'w-8 h-8 rounded-full bg-white border border-black/10 text-xs flex items-center justify-center text-[#1D1D1F] shrink-0 transition';
      hdr.appendChild(btn);
      applyTheme(localStorage.getItem('med_theme') === 'dark');
    }
  });
})();
