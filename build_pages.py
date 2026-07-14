import os

base_path = r'c:\Users\Siddhant\OneDrive\图片\Desktop\scholarship\frontend\pages'

def get_base_html(title, page_name, content):
    sidebar_items = [
        ('student-dashboard.html', 'Dashboard', 'fa-house', page_name == 'dashboard'),
        ('scholarships.html', 'Explore Scholarships', 'fa-magnifying-glass-dollar', page_name == 'scholarships'),
        ('applications.html', 'My Applications', 'fa-file-contract', page_name == 'applications'),
        ('section_Tools', '', '', False),
        ('funding-planner.html', 'Funding Planner', 'fa-calculator', page_name == 'funding-planner'),
        ('ai-chat.html', 'AI Assistant', 'fa-robot', page_name == 'ai-chat'),
        ('career.html', 'Career Guidance', 'fa-briefcase', page_name == 'career'),
        ('documents.html', 'Document Vault', 'fa-folder-open', page_name == 'documents'),
    ]

    sidebar_html = ""
    for item in sidebar_items:
        if item[0].startswith('section_'):
            sidebar_html += f'\n        <span class="sidebar-section-label">{item[1] if item[1] else "Tools"}</span>'
        else:
            active_class = ' active' if item[3] else ''
            sidebar_html += f'''
        <a href="{item[0]}" class="nav-item{active_class}">
            <div class="nav-item-icon"><i class="fa-solid {item[2]}"></i></div>
            <span>{item[1]}</span>
        </a>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | EduBridge AI</title>
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        {sidebar_html}

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
            {content}
        </div>
    </main>
</div>

<!-- Toast Container -->
<div class="toast-container" id="toastContainer"></div>

<script src="../js/core/api.js"></script>
<script>
function toggleSidebar() {{
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('active');
}}
function handleLogout(e) {{
    e.preventDefault();
    if (typeof API !== 'undefined' && API.logout) API.logout();
    else {{ localStorage.clear(); window.location.href = 'login.html'; }}
}}
</script>
</body>
</html>'''

# 1. Applications Page
applications_content = '''
            <div class="top-header animate-fade-up">
                <div>
                    <h1 class="page-title">My Applications</h1>
                    <p class="page-subtitle">Track and manage your scholarship submissions.</p>
                </div>
                <div class="header-actions">
                    <a href="scholarships.html" class="btn btn-primary">
                        <i class="fa-solid fa-plus"></i> New Application
                    </a>
                </div>
            </div>

            <!-- STATS -->
            <div class="stats-grid animate-fade-up delay-1">
                <div class="stat-card">
                    <div class="stat-card-icon blue"><i class="fa-solid fa-file-contract"></i></div>
                    <div class="stat-card-value">6</div>
                    <div class="stat-card-label">Total Applications</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-icon orange"><i class="fa-solid fa-clock-rotate-left"></i></div>
                    <div class="stat-card-value">2</div>
                    <div class="stat-card-label">Under Review</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-icon green"><i class="fa-solid fa-check-circle"></i></div>
                    <div class="stat-card-value">1</div>
                    <div class="stat-card-label">Approved</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-icon" style="background:rgba(239,68,68,0.15);color:var(--clr-danger);"><i class="fa-solid fa-xmark-circle"></i></div>
                    <div class="stat-card-value">1</div>
                    <div class="stat-card-label">Rejected</div>
                </div>
            </div>

            <!-- FILTER BAR -->
            <div class="filter-bar animate-fade-up delay-2">
                <div class="filter-search input-icon-wrap">
                    <i class="input-icon fa-solid fa-magnifying-glass"></i>
                    <input type="text" class="form-control" placeholder="Search applications...">
                </div>
                <select class="filter-select">
                    <option value="">All Statuses</option>
                    <option value="approved">Approved</option>
                    <option value="under_review">Under Review</option>
                    <option value="submitted">Submitted</option>
                    <option value="rejected">Rejected</option>
                </select>
                <button class="btn btn-ghost btn-sm"><i class="fa-solid fa-filter"></i> Filter</button>
            </div>

            <!-- APPS LIST -->
            <div class="flex-col gap-4 animate-fade-up delay-3">
                
                <div class="glass-card flex-between" style="padding:var(--sp-4) var(--sp-5);">
                    <div class="flex gap-4" style="align-items:center; flex:1;">
                        <div class="stat-card-icon purple" style="width:48px;height:48px;margin:0;"><i class="fa-solid fa-landmark"></i></div>
                        <div>
                            <h3 style="margin-bottom:2px;">NSP Scholarship</h3>
                            <div class="text-muted" style="font-size:0.85rem;">Central Govt • Applied: 10 Oct 2024</div>
                        </div>
                    </div>
                    <div style="width:120px;"><div class="badge badge-warning">Under Review</div></div>
                    <div style="width:100px;font-weight:700;">₹50,000</div>
                    <div style="width:120px;text-align:right;">
                        <button class="btn btn-ghost btn-sm">View Details</button>
                    </div>
                </div>

                <div class="glass-card flex-between" style="padding:var(--sp-4) var(--sp-5);">
                    <div class="flex gap-4" style="align-items:center; flex:1;">
                        <div class="stat-card-icon blue" style="width:48px;height:48px;margin:0;"><i class="fa-solid fa-building"></i></div>
                        <div>
                            <h3 style="margin-bottom:2px;">Tata Capital Pankh</h3>
                            <div class="text-muted" style="font-size:0.85rem;">Corporate CSR • Applied: 05 Sep 2024</div>
                        </div>
                    </div>
                    <div style="width:120px;"><div class="badge badge-success">Approved</div></div>
                    <div style="width:100px;font-weight:700;">₹12,000</div>
                    <div style="width:120px;text-align:right;">
                        <button class="btn btn-primary btn-sm">Claim Fund</button>
                    </div>
                </div>

                <div class="glass-card flex-between" style="padding:var(--sp-4) var(--sp-5);">
                    <div class="flex gap-4" style="align-items:center; flex:1;">
                        <div class="stat-card-icon green" style="width:48px;height:48px;margin:0;"><i class="fa-solid fa-leaf"></i></div>
                        <div>
                            <h3 style="margin-bottom:2px;">INSPIRE DST</h3>
                            <div class="text-muted" style="font-size:0.85rem;">Central Govt • Applied: 01 Nov 2024</div>
                        </div>
                    </div>
                    <div style="width:120px;"><div class="badge badge-info">Submitted</div></div>
                    <div style="width:100px;font-weight:700;">₹80,000</div>
                    <div style="width:120px;text-align:right;">
                        <button class="btn btn-ghost btn-sm">View Details</button>
                    </div>
                </div>
                
                 <div class="glass-card flex-between" style="padding:var(--sp-4) var(--sp-5);">
                    <div class="flex gap-4" style="align-items:center; flex:1;">
                        <div class="stat-card-icon" style="background:rgba(239,68,68,0.15);color:var(--clr-danger);width:48px;height:48px;margin:0;"><i class="fa-solid fa-xmark"></i></div>
                        <div>
                            <h3 style="margin-bottom:2px;">PM-YASASVI</h3>
                            <div class="text-muted" style="font-size:0.85rem;">Central Govt • Applied: 15 Aug 2024</div>
                        </div>
                    </div>
                    <div style="width:120px;"><div class="badge badge-danger">Rejected</div></div>
                    <div style="width:100px;font-weight:700;">₹20,000</div>
                    <div style="width:120px;text-align:right;">
                        <button class="btn btn-ghost btn-sm">Read Reason</button>
                    </div>
                </div>

            </div>
'''
with open(os.path.join(base_path, 'applications.html'), 'w', encoding='utf-8') as f:
    f.write(get_base_html('My Applications', 'applications', applications_content))

# 2. Funding Planner Page
funding_content = '''
            <div class="top-header animate-fade-up">
                <div>
                    <h1 class="page-title">Funding Planner</h1>
                    <p class="page-subtitle">Calculate and plan your education finances effectively.</p>
                </div>
            </div>

            <div class="dashboard-grid animate-fade-up delay-1">
                <!-- LEFT: INPUT FORM -->
                <div class="glass-card">
                    <h3 class="mb-4">Financial Inputs</h3>
                    <div class="two-col-form" style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;">
                        <div class="form-group" style="margin:0;">
                            <label class="form-label">Total Course Fee (₹)</label>
                            <input type="number" id="feeInput" class="form-control" value="500000" oninput="calcFunding()">
                        </div>
                        <div class="form-group" style="margin:0;">
                            <label class="form-label">Duration (Years)</label>
                            <input type="number" id="durationInput" class="form-control" value="4" oninput="calcFunding()">
                        </div>
                        <div class="form-group" style="margin:0;">
                            <label class="form-label">Family Annual Income (₹)</label>
                            <input type="number" id="incomeInput" class="form-control" value="300000" oninput="calcFunding()">
                        </div>
                        <div class="form-group" style="margin:0;">
                            <label class="form-label">Expected Scholarships (₹)</label>
                            <input type="number" id="schInput" class="form-control" value="150000" oninput="calcFunding()">
                        </div>
                        <div class="form-group" style="margin:0;">
                            <label class="form-label">Self Funding / Savings (₹)</label>
                            <input type="number" id="selfInput" class="form-control" value="50000" oninput="calcFunding()">
                        </div>
                    </div>
                    <button class="btn btn-primary w-full mt-6" onclick="calcFunding()"><i class="fa-solid fa-calculator"></i> Calculate Plan</button>
                </div>

                <!-- RIGHT: RESULTS -->
                <div class="glass-card text-center flex-col gap-4">
                    <h3>Funding Breakdown</h3>
                    
                    <div style="position:relative;height:180px;width:100%;display:flex;justify-content:center;">
                        <canvas id="fundingChart"></canvas>
                        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:var(--font-display);font-weight:800;font-size:1.5rem;" id="gapLabel">...</div>
                    </div>
                    
                    <div class="divider"></div>

                    <div class="flex-between">
                        <span class="text-muted">Funding Gap (Loan Needed)</span>
                        <strong class="text-danger" style="font-size:1.2rem;" id="resGap">₹3,00,000</strong>
                    </div>
                    <div class="flex-between">
                        <span class="text-muted">Estimated EMI (8% over 5yrs)</span>
                        <strong style="font-size:1.1rem;" id="resEmi">₹6,082 /mo</strong>
                    </div>
                     <div class="flex-between">
                        <span class="text-muted">Scholarship Coverage</span>
                        <strong class="text-success" id="resCov">30%</strong>
                    </div>
                </div>
            </div>

            <!-- TIPS -->
            <h3 class="mb-4 mt-6 animate-fade-up delay-2">Quick Financial Tips</h3>
            <div class="three-col-grid animate-fade-up delay-3">
                <div class="glass-card">
                    <div class="stat-card-icon purple"><i class="fa-solid fa-graduation-cap"></i></div>
                    <h4 class="mb-2">Maximize Scholarships</h4>
                    <p class="text-muted" style="font-size:0.85rem;">You are covering 30% of your fee via scholarships. Try applying to Corporate CSR grants to push this to 50%.</p>
                </div>
                <div class="glass-card">
                    <div class="stat-card-icon blue"><i class="fa-solid fa-building-columns"></i></div>
                    <h4 class="mb-2">Education Loans</h4>
                    <p class="text-muted" style="font-size:0.85rem;">With a family income of ₹3L, you are eligible for the Vidyalakshmi portal interest-subsidy schemes (CSIS).</p>
                </div>
                <div class="glass-card">
                    <div class="stat-card-icon green"><i class="fa-solid fa-piggy-bank"></i></div>
                    <h4 class="mb-2">Smart Savings</h4>
                    <p class="text-muted" style="font-size:0.85rem;">Investing a small amount monthly in recurring deposits can help offset your living expenses during studies.</p>
                </div>
            </div>

            <script>
                let chart = null;
                function calcFunding() {
                    const fee = parseFloat(document.getElementById('feeInput').value) || 0;
                    const sch = parseFloat(document.getElementById('schInput').value) || 0;
                    const self = parseFloat(document.getElementById('selfInput').value) || 0;
                    
                    let gap = fee - sch - self;
                    if(gap < 0) gap = 0;
                    
                    document.getElementById('resGap').innerText = "₹" + gap.toLocaleString('en-IN');
                    
                    // Simple EMI roughly: gap * (rate)
                    const r = 0.08 / 12; // 8% monthly
                    const n = 60; // 5 years
                    let emi = 0;
                    if(gap > 0) {
                        emi = gap * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1);
                    }
                    document.getElementById('resEmi').innerText = "₹" + Math.round(emi).toLocaleString('en-IN') + " /mo";
                    
                    const cov = fee > 0 ? Math.round((sch / fee) * 100) : 0;
                    document.getElementById('resCov').innerText = cov + "%";
                    
                    document.getElementById('gapLabel').innerText = gap > 0 ? "Gap" : "Funded";
                    document.getElementById('gapLabel').style.color = gap > 0 ? "var(--clr-danger)" : "var(--clr-success)";

                    updateChart(sch, self, gap);
                }

                function updateChart(sch, self, gap) {
                    const ctx = document.getElementById('fundingChart').getContext('2d');
                    if(chart) chart.destroy();
                    chart = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: ['Scholarships', 'Self Funding', 'Gap (Loan)'],
                            datasets: [{
                                data: [sch, self, gap],
                                backgroundColor: ['#10B981', '#3B82F6', '#EF4444'],
                                borderWidth: 0,
                                hoverOffset: 4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            cutout: '75%',
                            plugins: {
                                legend: { display: false }
                            }
                        }
                    });
                }
                setTimeout(calcFunding, 500);
            </script>
'''
with open(os.path.join(base_path, 'funding-planner.html'), 'w', encoding='utf-8') as f:
    f.write(get_base_html('Funding Planner', 'funding-planner', funding_content))

# 3. AI Chat Page
ai_chat_content = '''
            <div class="top-header animate-fade-up">
                <div>
                    <h1 class="page-title">AI Financial Assistant</h1>
                    <p class="page-subtitle">Ask anything about scholarships, deadlines, and financial aid.</p>
                </div>
            </div>

            <div class="chat-layout animate-fade-up delay-1">
                <!-- Chat Messages -->
                <div class="chat-messages" id="chatWindow">
                    
                    <div class="chat-bubble ai">
                        <div style="font-weight:700;margin-bottom:6px;color:var(--text-primary);"><i class="fa-solid fa-robot"></i> EduBridge AI</div>
                        Welcome! I am your AI financial copilot. I can help you find scholarships, plan your finances, and guide your applications. What would you like to know?
                    </div>

                    <div class="chat-bubble user">
                        What scholarships are available for engineering students from UP?
                    </div>

                    <div class="chat-bubble ai">
                        <div style="font-weight:700;margin-bottom:6px;color:var(--text-primary);"><i class="fa-solid fa-robot"></i> EduBridge AI</div>
                        Based on your profile (Engineering student in Uttar Pradesh), here are the top 4 scholarships you should target:
                        <ul style="margin-top:10px;padding-left:20px;">
                            <li style="margin-bottom:8px;"><strong>UP State Scholarship Portal (Post-Matric):</strong> Covers up to ₹50,000 annually. Open for SC/ST/OBC/Gen(EWS).</li>
                            <li style="margin-bottom:8px;"><strong>AICTE PRAGATI:</strong> For female engineering students (₹50,000/year).</li>
                            <li style="margin-bottom:8px;"><strong>NSP Post Matric (Central):</strong> General post-matric scheme.</li>
                            <li style="margin-bottom:8px;"><strong>HDFC Badhte Kadam (Corporate):</strong> CSR initiative for general undergrads.</li>
                        </ul>
                        Would you like the direct application links for any of these?
                    </div>

                </div>

                <!-- Suggested Prompts -->
                <div style="padding:var(--sp-2) var(--sp-5);display:flex;gap:var(--sp-2);overflow-x:auto;">
                    <button class="badge badge-neutral" style="cursor:pointer;font-weight:500;padding:6px 12px;text-transform:none;" onclick="sendMockMsg('Calculate my funding gap for 4 years')">Calculate my funding gap</button>
                    <button class="badge badge-neutral" style="cursor:pointer;font-weight:500;padding:6px 12px;text-transform:none;" onclick="sendMockMsg('What documents do I need for NSP?')">Documents needed for NSP?</button>
                    <button class="badge badge-neutral" style="cursor:pointer;font-weight:500;padding:6px 12px;text-transform:none;" onclick="sendMockMsg('Find scholarships matching my profile')">Find scholarships for my profile</button>
                </div>

                <!-- Input Area -->
                <div class="chat-input-bar">
                    <input type="text" id="chatInput" class="form-control" placeholder="Ask EduBridge AI..." onkeypress="handleEnter(event)">
                    <button class="btn btn-primary" onclick="sendMessage()"><i class="fa-solid fa-paper-plane"></i></button>
                </div>
            </div>

            <script>
                function handleEnter(e) {
                    if(e.key === 'Enter') sendMessage();
                }

                function sendMockMsg(text) {
                    document.getElementById('chatInput').value = text;
                    sendMessage();
                }

                function sendMessage() {
                    const input = document.getElementById('chatInput');
                    const text = input.value.trim();
                    if(!text) return;

                    const chat = document.getElementById('chatWindow');
                    
                    // User message
                    const userDiv = document.createElement('div');
                    userDiv.className = 'chat-bubble user animate-fade-up';
                    userDiv.innerText = text;
                    chat.appendChild(userDiv);

                    input.value = '';
                    chat.scrollTop = chat.scrollHeight;

                    // Fake AI response
                    setTimeout(() => {
                        const aiDiv = document.createElement('div');
                        aiDiv.className = 'chat-bubble ai animate-fade-up';
                        aiDiv.innerHTML = `<div style="font-weight:700;margin-bottom:6px;color:var(--text-primary);"><i class="fa-solid fa-robot"></i> EduBridge AI</div>` + 
                            `I'm currently running in a demo environment. In production, I would connect to the Gemini API to analyze your query: "<i>${text}</i>" and provide real-time personalized guidance from the EduBridge scholarship database.`;
                        chat.appendChild(aiDiv);
                        chat.scrollTop = chat.scrollHeight;
                    }, 800);
                }
            </script>
'''
with open(os.path.join(base_path, 'ai-chat.html'), 'w', encoding='utf-8') as f:
    f.write(get_base_html('AI Assistant', 'ai-chat', ai_chat_content))

# 4. Career Page
career_content = '''
            <div class="top-header animate-fade-up">
                <div>
                    <h1 class="page-title">Career Guidance</h1>
                    <p class="page-subtitle">Explore career paths and discover funding specific to your goals.</p>
                </div>
            </div>

            <!-- Featured Banner -->
            <div class="animate-fade-up delay-1" style="
                background: var(--grad-brand-vivid);
                border-radius: var(--r-2xl);
                padding: var(--sp-8);
                margin-bottom: var(--sp-8);
                display:flex;
                justify-content:space-between;
                align-items:center;
                position:relative;
                overflow:hidden;
            ">
                <div style="position:relative;z-index:1;">
                    <div class="badge badge-primary mb-4" style="background:rgba(0,0,0,0.3);color:#fff;border:none;">Featured Path</div>
                    <h2 style="font-size:2rem;color:#fff;margin-bottom:var(--sp-2);">Technology & Engineering</h2>
                    <p style="color:rgba(255,255,255,0.8);max-width:500px;margin-bottom:var(--sp-4);">
                        Discover top opportunities in AI, Data Science, and core engineering. 
                        Over 45 specialized scholarships available for this track.
                    </p>
                    <button class="btn btn-primary" style="background:#fff;color:var(--clr-primary);"><i class="fa-solid fa-compass"></i> Explore Tech Path</button>
                </div>
                <i class="fa-solid fa-microchip" style="font-size:12rem;color:rgba(255,255,255,0.1);position:absolute;right:2rem;top:-2rem;"></i>
            </div>

            <!-- Categories -->
            <h3 class="mb-4 animate-fade-up delay-2">Career Categories</h3>
            <div class="three-col-grid animate-fade-up delay-3 mb-8">
                <div class="glass-card">
                    <div class="stat-card-icon purple"><i class="fa-solid fa-laptop-code"></i></div>
                    <h4 class="mb-1">Technology & IT</h4>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">45 Scholarships available</p>
                    <button class="btn btn-ghost btn-sm w-full">View Details</button>
                </div>
                <div class="glass-card">
                    <div class="stat-card-icon green"><i class="fa-solid fa-stethoscope"></i></div>
                    <h4 class="mb-1">Medicine & Healthcare</h4>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">32 Scholarships available</p>
                    <button class="btn btn-ghost btn-sm w-full">View Details</button>
                </div>
                <div class="glass-card">
                    <div class="stat-card-icon blue"><i class="fa-solid fa-scale-balanced"></i></div>
                    <h4 class="mb-1">Law & Social Sciences</h4>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">18 Scholarships available</p>
                    <button class="btn btn-ghost btn-sm w-full">View Details</button>
                </div>
                 <div class="glass-card">
                    <div class="stat-card-icon orange"><i class="fa-solid fa-chart-line"></i></div>
                    <h4 class="mb-1">Business & Management</h4>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">24 Scholarships available</p>
                    <button class="btn btn-ghost btn-sm w-full">View Details</button>
                </div>
                 <div class="glass-card">
                    <div class="stat-card-icon" style="background:rgba(239,68,68,0.15);color:var(--clr-danger);"><i class="fa-solid fa-flask"></i></div>
                    <h4 class="mb-1">Research & Academia</h4>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">28 Fellowships available</p>
                    <button class="btn btn-ghost btn-sm w-full">View Details</button>
                </div>
                 <div class="glass-card">
                    <div class="stat-card-icon" style="background:rgba(6,182,212,0.15);color:var(--clr-info);"><i class="fa-solid fa-palette"></i></div>
                    <h4 class="mb-1">Arts & Design</h4>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">15 Scholarships available</p>
                    <button class="btn btn-ghost btn-sm w-full">View Details</button>
                </div>
            </div>

            <!-- Resources -->
            <h3 class="mb-4 animate-fade-up delay-4">Career Resources</h3>
            <div class="three-col-grid animate-fade-up delay-5">
                <div class="glass-card flex gap-4" style="align-items:center;">
                    <div class="stat-card-icon" style="margin:0;flex-shrink:0;"><i class="fa-solid fa-file-lines"></i></div>
                    <div>
                        <h4 style="margin-bottom:2px;">Resume Builder</h4>
                        <div class="text-muted" style="font-size:0.8rem;margin-bottom:8px;">AI-powered CV creation</div>
                        <a href="#" class="text-primary" style="font-size:0.85rem;font-weight:600;">Start Building &rarr;</a>
                    </div>
                </div>
                <div class="glass-card flex gap-4" style="align-items:center;">
                    <div class="stat-card-icon" style="margin:0;flex-shrink:0;"><i class="fa-solid fa-users"></i></div>
                    <div>
                        <h4 style="margin-bottom:2px;">Interview Prep</h4>
                        <div class="text-muted" style="font-size:0.8rem;margin-bottom:8px;">Mock interviews via AI</div>
                        <a href="#" class="text-primary" style="font-size:0.85rem;font-weight:600;">Practice Now &rarr;</a>
                    </div>
                </div>
                <div class="glass-card flex gap-4" style="align-items:center;">
                    <div class="stat-card-icon" style="margin:0;flex-shrink:0;"><i class="fa-brands fa-linkedin"></i></div>
                    <div>
                        <h4 style="margin-bottom:2px;">LinkedIn Opt.</h4>
                        <div class="text-muted" style="font-size:0.8rem;margin-bottom:8px;">Enhance your profile</div>
                        <a href="#" class="text-primary" style="font-size:0.85rem;font-weight:600;">Review Profile &rarr;</a>
                    </div>
                </div>
            </div>
'''
with open(os.path.join(base_path, 'career.html'), 'w', encoding='utf-8') as f:
    f.write(get_base_html('Career Guidance', 'career', career_content))

# 5. Documents Page
docs_content = '''
            <div class="top-header animate-fade-up">
                <div>
                    <h1 class="page-title">Document Vault</h1>
                    <p class="page-subtitle">Securely store and AI-verify your scholarship documents.</p>
                </div>
            </div>

            <!-- Upload Zone -->
            <div class="glass-card animate-fade-up delay-1 text-center" style="border: 2px dashed rgba(124,77,255,0.4); padding:4rem 2rem; margin-bottom:var(--sp-8); cursor:pointer; transition:all .3s; background:rgba(124,77,255,0.05);" onmouseover="this.style.background='rgba(124,77,255,0.1)';" onmouseout="this.style.background='rgba(124,77,255,0.05)';">
                <i class="fa-solid fa-cloud-arrow-up" style="font-size:3.5rem;color:var(--clr-primary-light);margin-bottom:1rem;"></i>
                <h3 class="mb-2">Drag & Drop Documents Here</h3>
                <p class="text-muted mb-4">Supported formats: PDF, JPG, PNG (Max 5MB)</p>
                <button class="btn btn-primary"><i class="fa-solid fa-folder-open"></i> Browse Files</button>
            </div>

            <div class="dashboard-grid">
                <!-- Document List -->
                <div class="glass-card animate-fade-up delay-2">
                    <h3 class="mb-4">My Documents</h3>
                    
                    <div class="flex-col gap-3">
                        <div class="notif-item" style="align-items:center;">
                            <div class="notif-icon purple" style="font-size:1.5rem;"><i class="fa-solid fa-file-pdf"></i></div>
                            <div style="flex:1;">
                                <div style="font-weight:600;">Aadhaar Card</div>
                                <div class="text-muted" style="font-size:0.8rem;">245 KB • Uploaded Oct 10</div>
                            </div>
                            <div class="badge badge-success"><i class="fa-solid fa-check"></i> Verified</div>
                            <button class="btn btn-ghost btn-sm btn-icon"><i class="fa-solid fa-eye"></i></button>
                        </div>

                        <div class="notif-item" style="align-items:center;">
                            <div class="notif-icon purple" style="font-size:1.5rem;"><i class="fa-solid fa-file-pdf"></i></div>
                            <div style="flex:1;">
                                <div style="font-weight:600;">Income Certificate</div>
                                <div class="text-muted" style="font-size:0.8rem;">1.2 MB • Uploaded Oct 12</div>
                            </div>
                            <div class="badge badge-success"><i class="fa-solid fa-check"></i> Verified</div>
                            <button class="btn btn-ghost btn-sm btn-icon"><i class="fa-solid fa-eye"></i></button>
                        </div>

                        <div class="notif-item" style="align-items:center;">
                            <div class="notif-icon purple" style="font-size:1.5rem;"><i class="fa-solid fa-file-pdf"></i></div>
                            <div style="flex:1;">
                                <div style="font-weight:600;">10th Marksheet</div>
                                <div class="text-muted" style="font-size:0.8rem;">890 KB • Uploaded Oct 12</div>
                            </div>
                            <div class="badge badge-success"><i class="fa-solid fa-check"></i> Verified</div>
                            <button class="btn btn-ghost btn-sm btn-icon"><i class="fa-solid fa-eye"></i></button>
                        </div>

                        <div class="notif-item" style="align-items:center;">
                            <div class="notif-icon purple" style="font-size:1.5rem;"><i class="fa-solid fa-file-image"></i></div>
                            <div style="flex:1;">
                                <div style="font-weight:600;">12th Marksheet</div>
                                <div class="text-muted" style="font-size:0.8rem;">1.1 MB • Uploaded Today</div>
                            </div>
                            <div class="badge badge-warning"><i class="fa-solid fa-clock"></i> AI Reviewing</div>
                            <button class="btn btn-ghost btn-sm btn-icon"><i class="fa-solid fa-eye"></i></button>
                        </div>

                        <div class="notif-item" style="align-items:center;">
                            <div class="notif-icon" style="font-size:1.5rem;background:var(--bg-hover);color:var(--text-muted)"><i class="fa-solid fa-file-circle-xmark"></i></div>
                            <div style="flex:1;">
                                <div style="font-weight:600;color:var(--text-muted)">Caste Certificate</div>
                                <div class="text-muted" style="font-size:0.8rem;">Required for SC/ST</div>
                            </div>
                            <div class="badge badge-neutral">Missing</div>
                            <button class="btn btn-primary btn-sm" style="padding:0.4rem 0.8rem;">Upload</button>
                        </div>
                    </div>
                </div>

                <!-- Checklist -->
                <div class="glass-card animate-fade-up delay-3">
                    <h3 class="mb-4">NSP Checklist</h3>
                    <p class="text-muted mb-4" style="font-size:0.85rem;">Documents required for National Scholarship Portal (Post-Matric):</p>
                    
                    <div class="flex-col gap-3">
                        <label class="flex gap-2" style="align-items:center;cursor:pointer;">
                            <input type="checkbox" checked disabled> <span style="font-weight:500;">Aadhaar Card</span>
                        </label>
                        <label class="flex gap-2" style="align-items:center;cursor:pointer;">
                            <input type="checkbox" checked disabled> <span style="font-weight:500;">Income Certificate</span>
                        </label>
                        <label class="flex gap-2" style="align-items:center;cursor:pointer;">
                            <input type="checkbox" checked disabled> <span style="font-weight:500;">Previous Marksheet</span>
                        </label>
                        <label class="flex gap-2" style="align-items:center;cursor:pointer;">
                            <input type="checkbox"> <span style="font-weight:500;">Bank Passbook</span>
                        </label>
                        <label class="flex gap-2" style="align-items:center;cursor:pointer;">
                            <input type="checkbox"> <span style="font-weight:500;">Fee Receipt</span>
                        </label>
                        <label class="flex gap-2" style="align-items:center;cursor:pointer;">
                            <input type="checkbox"> <span style="font-weight:500;">Bonafide Certificate</span>
                        </label>
                    </div>

                    <div class="mt-6 p-4 rounded" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);">
                        <div class="text-success" style="font-weight:700;margin-bottom:4px;"><i class="fa-solid fa-shield-halved"></i> 50% Ready</div>
                        <div style="font-size:0.8rem;color:var(--text-muted)">Upload 3 more documents to complete your NSP profile.</div>
                    </div>
                </div>
            </div>
'''
with open(os.path.join(base_path, 'documents.html'), 'w', encoding='utf-8') as f:
    f.write(get_base_html('Document Vault', 'documents', docs_content))

print("All 5 dashboard pages built successfully!")
