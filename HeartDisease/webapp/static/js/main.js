/* ─── Smooth Scroll & Navigation ─── */
document.addEventListener('DOMContentLoaded', () => {

    // ── Navbar scroll effect ──
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    // ── Mobile toggle ──
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            mobileToggle.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
        });

        // Close menu on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                mobileToggle.textContent = '☰';
            });
        });
    }

    // ── Fade-in on scroll ──
    const fadeElements = document.querySelectorAll('.fade-in');
    if (fadeElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(el => observer.observe(el));
    }

    // ── Data table search ──
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('input', filterTable);
    }

    // ── Data table filter select ──
    const filterSelect = document.getElementById('diagnosisFilter');
    if (filterSelect) {
        filterSelect.addEventListener('change', filterTable);
    }

    const genderFilter = document.getElementById('genderFilter');
    if (genderFilter) {
        genderFilter.addEventListener('change', filterTable);
    }
});

/* ─── Table Filtering ─── */
function filterTable() {
    const searchTerm = (document.getElementById('tableSearch')?.value || '').toLowerCase();
    const diagnosisFilter = document.getElementById('diagnosisFilter')?.value || 'all';
    const genderFilter = document.getElementById('genderFilter')?.value || 'all';
    const rows = document.querySelectorAll('.data-table tbody tr');
    let visibleCount = 0;

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const diagnosis = row.dataset.diagnosis || '';
        const gender = row.dataset.gender || '';

        const matchesSearch = text.includes(searchTerm);
        const matchesDiagnosis = diagnosisFilter === 'all' || diagnosis === diagnosisFilter;
        const matchesGender = genderFilter === 'all' || gender === genderFilter;

        if (matchesSearch && matchesDiagnosis && matchesGender) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    // Update count
    const countEl = document.getElementById('resultCount');
    if (countEl) {
        countEl.textContent = `${visibleCount} records`;
    }
}

/* ─── Smooth scroll for anchor links ─── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
