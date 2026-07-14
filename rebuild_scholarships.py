"""
Rebuild the scholarships.html page with the new design system.
Reads scholarship data from scholarships_data.js and creates a premium new page.
"""
import re

# Read existing scholarship data
with open('scholarships_data.js', 'r', encoding='utf-8') as f:
    raw = f.read()

# Extract just the array part (remove 'const scholarships = ' prefix and trailing ;)
array_str = raw.replace('const scholarships = ', '', 1).rstrip().rstrip(';')

new_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scholarship Explorer | EduBridge AI</title>
    <meta name="description" content="Explore 100+ scholarships tailored to your academic profile with AI-powered matching.">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>

<!-- Mobile Top Bar -->
<div class="mobile-topbar" id="mobileTopbar">
    <button class="hamburger-btn" onclick="toggleSidebar()" aria-label="Open menu">
        <i class="fa-solid fa-bars"></i>
    </button>
    <span style="font-family:var(--font-display);font-weight:800;font-size:1.1rem;">EduBridge AI</span>
    <div class="avatar" style="width:36px;height:36px;font-size:.85rem;">S</div>
</div>
<div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>

<div class="dashboard-layout">
    <!-- ═══ SIDEBAR ═══ -->
    <aside class="sidebar" id="sidebar">
        <a href="../../index.html" class="sidebar-brand">
            <div class="sidebar-brand-icon"><i class="fa-solid fa-graduation-cap"></i></div>
            <span class="sidebar-brand-text">EduBridge AI</span>
        </a>

        <span class="sidebar-section-label">Main Navigation</span>

        <a href="student-dashboard.html" class="nav-item">
            <div class="nav-item-icon"><i class="fa-solid fa-house"></i></div>
            <span>Dashboard</span>
        </a>
        <a href="scholarships.html" class="nav-item active">
            <div class="nav-item-icon"><i class="fa-solid fa-magnifying-glass-dollar"></i></div>
            <span>Explore Scholarships</span>
        </a>
        <a href="applications.html" class="nav-item">
            <div class="nav-item-icon"><i class="fa-solid fa-file-contract"></i></div>
            <span>My Applications</span>
        </a>

        <span class="sidebar-section-label">Tools</span>

        <a href="funding-planner.html" class="nav-item">
            <div class="nav-item-icon"><i class="fa-solid fa-calculator"></i></div>
            <span>Funding Planner</span>
        </a>
        <a href="ai-chat.html" class="nav-item">
            <div class="nav-item-icon"><i class="fa-solid fa-robot"></i></div>
            <span>AI Assistant</span>
        </a>
        <a href="career.html" class="nav-item">
            <div class="nav-item-icon"><i class="fa-solid fa-briefcase"></i></div>
            <span>Career Guidance</span>
        </a>
        <a href="documents.html" class="nav-item">
            <div class="nav-item-icon"><i class="fa-solid fa-folder-open"></i></div>
            <span>Document Vault</span>
        </a>

        <div class="sidebar-footer">
            <a href="#" class="nav-item" onclick="handleLogout(event)">
                <div class="nav-item-icon" style="color:var(--clr-danger)"><i class="fa-solid fa-arrow-right-from-bracket"></i></div>
                <span>Logout</span>
            </a>
        </div>
    </aside>

    <!-- ═══ MAIN CONTENT ═══ -->
    <main class="main-content">
        <div class="page-content">

            <!-- Top Header -->
            <div class="top-header animate-fade-up">
                <div>
                    <h1 class="page-title">Scholarship Explorer</h1>
                    <p class="page-subtitle" id="scholarshipCount">Loading scholarships...</p>
                </div>
                <div class="header-actions">
                    <div style="background:var(--bg-elevated);border:1px solid var(--border-soft);border-radius:var(--r-full);padding:6px 14px;font-size:.82rem;color:var(--text-muted);display:flex;align-items:center;gap:6px;">
                        <i class="fa-solid fa-wand-magic-sparkles" style="color:var(--clr-primary-light)"></i>
                        AI Powered Matching
                    </div>
                </div>
            </div>

            <!-- Filter Bar -->
            <div class="filter-bar animate-fade-up delay-1">
                <div class="filter-search input-icon-wrap">
                    <i class="input-icon fa-solid fa-magnifying-glass"></i>
                    <input type="text" class="form-control filter-input" id="searchInput"
                        placeholder="Search by name, provider, or keyword..."
                        oninput="filterScholarships()">
                </div>
                <select class="filter-select" id="typeFilter" onchange="filterScholarships()">
                    <option value="">All Categories</option>
                    <option value="government">Government</option>
                    <option value="csr">CSR / Corporate</option>
                    <option value="ngo">NGO / Foundation</option>
                    <option value="international">International</option>
                    <option value="psu">PSU</option>
                    <option value="university">University</option>
                </select>
                <select class="filter-select" id="sortFilter" onchange="filterScholarships()">
                    <option value="fit">Sort: Best Match</option>
                    <option value="amount_high">Sort: Highest Amount</option>
                    <option value="amount_low">Sort: Lowest Amount</option>
                    <option value="name">Sort: Name A-Z</option>
                </select>
                <button class="btn btn-ghost btn-sm" onclick="resetFilters()" style="white-space:nowrap">
                    <i class="fa-solid fa-rotate-left"></i> Reset
                </button>
            </div>

            <!-- Stats Bar -->
            <div class="flex gap-3 mb-6 animate-fade-up delay-2" id="statsBar" style="flex-wrap:wrap;">
                <div class="badge badge-primary" style="padding:.5rem 1rem;font-size:.8rem;" id="countBadge">0 scholarships</div>
                <div class="badge badge-success" style="padding:.5rem 1rem;font-size:.8rem;">Upto ₹10L available</div>
                <div class="badge badge-info" style="padding:.5rem 1rem;font-size:.8rem;"><i class="fa-solid fa-robot"></i> AI-Matched</div>
            </div>

            <!-- Scholarship Grid -->
            <div class="scholarship-grid animate-fade-up delay-3" id="scholarshipsContainer">
                <div style="grid-column:1/-1;text-align:center;padding:5rem;color:var(--text-muted);">
                    <i class="fa-solid fa-circle-notch fa-spin" style="font-size:2rem;margin-bottom:1rem;display:block;color:var(--clr-primary-light);"></i>
                    <p>AI is analyzing your profile to find best matches...</p>
                </div>
            </div>

            <!-- Load More -->
            <div class="text-center mt-8" id="loadMoreWrap" style="display:none;">
                <button class="btn btn-ghost btn-lg" id="loadMoreBtn" onclick="loadMore()">
                    <i class="fa-solid fa-chevron-down"></i> Load More Scholarships
                </button>
            </div>

        </div>
    </main>
</div>

<!-- Toast Container -->
<div class="toast-container" id="toastContainer"></div>

<script src="../js/core/api.js"></script>
<script>
// ══════════════════════════════════════════
//  Scholarship Explorer JS — EduBridge AI v3
// ══════════════════════════════════════════

const SCHOLARSHIPS_PER_PAGE = 12;
let currentPage = 1;
let filteredData = [];

// Type mapping for display
const typeLabels = {
    government:   { label: 'Government',   badgeClass: 'badge-info' },
    csr:          { label: 'Corporate/CSR', badgeClass: 'badge-warning' },
    ngo:          { label: 'NGO/Foundation',badgeClass: 'badge-success' },
    international:{ label: 'International', badgeClass: 'badge-primary' },
    psu:          { label: 'PSU',           badgeClass: 'badge-neutral' },
    university:   { label: 'University',    badgeClass: 'badge-danger' }
};

// ── Sidebar Toggle ──
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('active');
}

// ── Logout ──
function handleLogout(e) {
    e.preventDefault();
    if (typeof API !== 'undefined' && API.logout) API.logout();
    else { localStorage.clear(); window.location.href = 'login.html'; }
}

// ── Toast ──
function showToast(msg, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = msg;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity='0'; toast.style.transform='translateX(120%)'; toast.style.transition='all .3s ease'; setTimeout(()=>toast.remove(),300); }, 4000);
}

// ── Format currency ──
function formatAmount(amount) {
    if (!amount) return 'Varies';
    if (amount >= 100000) return '₹' + (amount/100000).toFixed(1) + 'L';
    if (amount >= 1000)   return '₹' + (amount/1000).toFixed(0) + 'K';
    return '₹' + amount;
}

// ── Get fit badge ──
function getFitBadge(score) {
    if (!score) return '';
    const cls = score >= 85 ? 'badge-success' : score >= 70 ? 'badge-warning' : 'badge-neutral';
    return `<span class="badge ${cls}" title="AI Match Score">${score}% match</span>`;
}

// ── Render card ──
function renderCard(s) {
    const typeInfo = typeLabels[s.type] || typeLabels['ngo'];
    const reqText = s.requirement || 'Eligibility details not available.';
    const displayReq = reqText.length > 180 ? reqText.substring(0, 180) + '...' : reqText;

    return `
    <div class="sch-card" data-type="${s.type || ''}" data-name="${s.name || ''}">
        <div class="sch-top">
            <span class="badge ${typeInfo.badgeClass}">${typeInfo.label}</span>
            ${getFitBadge(s.fit_score)}
        </div>
        <div class="sch-name">${s.name}</div>
        <div class="sch-amount">${formatAmount(s.amount)}</div>
        <div class="sch-meta">
            <div class="sch-meta-item"><i class="fa-solid fa-building"></i> ${s.provider || 'Various'}</div>
            ${s.deadline ? `<div class="sch-meta-item"><i class="fa-solid fa-calendar"></i> ${s.deadline}</div>` : ''}
        </div>
        <div class="sch-requirement">
            <strong><i class="fa-solid fa-circle-check" style="margin-right:4px;"></i> Eligibility</strong>
            ${displayReq}
        </div>
        <div class="sch-actions">
            <a href="${s.url || '#'}" target="_blank" rel="noopener" class="btn btn-primary btn-sm" style="flex:1;">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> Apply Now
            </a>
            <button class="btn btn-ghost btn-sm btn-icon" title="Save scholarship" onclick="saveScholarship(this, '${s.name.replace(/'/g,"\\'")}')">
                <i class="fa-regular fa-bookmark"></i>
            </button>
        </div>
    </div>`;
}

// ── Save scholarship ──
function saveScholarship(btn, name) {
    const icon = btn.querySelector('i');
    if (icon.classList.contains('fa-regular')) {
        icon.classList.replace('fa-regular', 'fa-solid');
        btn.style.color = 'var(--clr-primary-light)';
        showToast(`<i class="fa-solid fa-bookmark" style="color:var(--clr-primary-light)"></i> Saved: ${name}`, 'info');
    } else {
        icon.classList.replace('fa-solid', 'fa-regular');
        btn.style.color = '';
    }
}

// ── Filter & sort ──
function filterScholarships() {
    const search   = document.getElementById('searchInput').value.toLowerCase().trim();
    const typeVal  = document.getElementById('typeFilter').value;
    const sortVal  = document.getElementById('sortFilter').value;

    filteredData = window.ALL_SCHOLARSHIPS.filter(s => {
        const matchesSearch = !search ||
            (s.name && s.name.toLowerCase().includes(search)) ||
            (s.provider && s.provider.toLowerCase().includes(search)) ||
            (s.requirement && s.requirement.toLowerCase().includes(search));
        const matchesType = !typeVal || s.type === typeVal;
        return matchesSearch && matchesType;
    });

    // Sort
    if (sortVal === 'fit')          filteredData.sort((a,b) => (b.fit_score||0) - (a.fit_score||0));
    else if (sortVal === 'amount_high') filteredData.sort((a,b) => (b.amount||0) - (a.amount||0));
    else if (sortVal === 'amount_low')  filteredData.sort((a,b) => (a.amount||0) - (b.amount||0));
    else if (sortVal === 'name')        filteredData.sort((a,b) => (a.name||'').localeCompare(b.name||''));

    currentPage = 1;
    renderPage();
    document.getElementById('countBadge').textContent = `${filteredData.length} scholarships`;
}

// ── Render current page ──
function renderPage() {
    const container = document.getElementById('scholarshipsContainer');
    const start = 0;
    const end   = currentPage * SCHOLARSHIPS_PER_PAGE;
    const visible = filteredData.slice(start, end);

    if (visible.length === 0) {
        container.innerHTML = `
        <div style="grid-column:1/-1;text-align:center;padding:5rem;color:var(--text-muted);">
            <i class="fa-solid fa-circle-xmark" style="font-size:2.5rem;margin-bottom:1rem;display:block;color:var(--clr-danger);opacity:.5;"></i>
            <h3 style="margin-bottom:.5rem;color:var(--text-muted);">No scholarships found</h3>
            <p style="font-size:.9rem;">Try adjusting your search or filters.</p>
        </div>`;
    } else {
        container.innerHTML = visible.map(s => renderCard(s)).join('');
    }

    const loadMoreWrap = document.getElementById('loadMoreWrap');
    loadMoreWrap.style.display = filteredData.length > end ? 'block' : 'none';
}

// ── Load more ──
function loadMore() {
    currentPage++;
    renderPage();
    document.getElementById('loadMoreBtn').innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Loading...';
    setTimeout(() => {
        document.getElementById('loadMoreBtn').innerHTML = '<i class="fa-solid fa-chevron-down"></i> Load More Scholarships';
    }, 400);
}

// ── Reset filters ──
function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('typeFilter').value = '';
    document.getElementById('sortFilter').value = 'fit';
    filterScholarships();
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
    const total = window.ALL_SCHOLARSHIPS ? window.ALL_SCHOLARSHIPS.length : 0;
    document.getElementById('scholarshipCount').textContent =
        `${total} AI-matched scholarships across Government, Corporate & International sources`;
    document.getElementById('countBadge').textContent = `${total} scholarships`;
    filteredData = [...(window.ALL_SCHOLARSHIPS || [])];
    filteredData.sort((a,b) => (b.fit_score||0) - (a.fit_score||0));
    renderPage();
});
</script>

<!-- Scholarship Data (loaded first) -->
<script>
window.ALL_SCHOLARSHIPS = """ + array_str + """;
</script>

</body>
</html>"""

with open(r'frontend/pages/scholarships.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Done! scholarships.html rebuilt. Size: {len(new_html):,} bytes")
