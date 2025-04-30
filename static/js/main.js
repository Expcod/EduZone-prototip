// Main JavaScript file for EduZone

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Auto-expand sidebar menu based on current URL
    const currentPath = window.location.pathname;
    
    // Handle subject menus
    const subjects = ['kimyo', 'fizika', 'matematika', 'biologiya'];
    subjects.forEach(subject => {
        if (currentPath.includes(`/${subject}/`)) {
            const subjectMenu = document.getElementById(`${subject}Submenu`);
            if (subjectMenu) {
                new bootstrap.Collapse(subjectMenu, { toggle: true });
                
                // Handle lab submenus
                if (currentPath.includes(`/${subject}/laboratoriya/`)) {
                    const labMenu = document.getElementById(`${subject}LabSubmenu`);
                    if (labMenu) {
                        new bootstrap.Collapse(labMenu, { toggle: true });
                    }
                }
            }
        }
    });
    
    // Handle grade menu
    if (currentPath.includes('/sinf/')) {
        const sinflarMenu = document.getElementById('sinflarSubmenu');
        if (sinflarMenu) {
            new bootstrap.Collapse(sinflarMenu, { toggle: true });
        }
    }

    // Theme toggler
    const themeToggler = document.querySelector('button i.bi-moon, button i.bi-sun');
    if (themeToggler) {
        themeToggler.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            if (document.body.classList.contains('dark-mode')) {
                this.classList.remove('bi-moon');
                this.classList.add('bi-sun');
                localStorage.setItem('theme', 'dark');
            } else {
                this.classList.remove('bi-sun');
                this.classList.add('bi-moon');
                localStorage.setItem('theme', 'light');
            }
        });

        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggler.classList.remove('bi-moon');
            themeToggler.classList.add('bi-sun');
        }
    }

    // Custom file input
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = this.files[0]?.name || 'No file chosen';
            const nextSibling = this.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    });
});

// Custom template filters for Django
// These would normally be in Django's templatetags, but we're simulating their behavior in JS
function filterBySubject(experiments, subject) {
    return experiments.filter(exp => exp.subject.id === subject.id);
}

function completedCount(userExperiments, experiments) {
    let count = 0;
    experiments.forEach(exp => {
        if (userExperiments[exp.id] === true) {
            count++;
        }
    });
    return count;
}

function getItem(obj, key) {
    return obj[key];
}