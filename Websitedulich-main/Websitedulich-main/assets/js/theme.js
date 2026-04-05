document.addEventListener('DOMContentLoaded', () => {
    // Inject floating button
    const btn = document.createElement('button');
    btn.className = 'theme-toggle-btn';
    btn.innerHTML = '<i class="fas fa-moon"></i>';
    btn.setAttribute('aria-label', 'Toggle Dark Mode');
    document.body.appendChild(btn);

    // Check local storage for theme
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        btn.innerHTML = '<i class="fas fa-sun"></i>';
    }

    // Toggle event
    btn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        let theme = 'light';
        if (document.body.classList.contains('dark-mode')) {
            theme = 'dark';
            btn.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            btn.innerHTML = '<i class="fas fa-moon"></i>';
        }
        localStorage.setItem('theme', theme);
    });
});
