import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure viewport meta is present
if 'name="viewport"' not in content:
    content = content.replace('<head>', '<head>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">')

# Add responsive CSS before </style>
responsive_css = '''
        @media (max-width: 768px) {
            .nav-container { flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; }
            .nav-brand { font-size: 1rem; }
            .nav-link { font-size: 0.75rem; padding: 0.4rem 0.6rem; }
            .main-container { padding: 0.8rem; }
            .page-header h1 { font-size: 1.2rem; }
            .trends-grid { grid-template-columns: 1fr; }
            .trend-card { padding: 0.8rem; }
            .trend-metrics { grid-template-columns: repeat(3, 1fr); gap: 4px; }
            #dashboard .trends-grid { grid-template-columns: 1fr; }
            .modal-content { max-width: 95%; padding: 1.2rem; }
            #analysis-content h3 { font-size: 1rem; }
            .form-control { font-size: 0.9rem; }
            .btn { padding: 0.6rem 1rem; font-size: 0.9rem; }
            h3 { font-size: 1rem; }
            .analytics-grid { grid-template-columns: 1fr; }
            #local-trends, #international-trends { width: 100%; }
        }
        @media (max-width: 480px) {
            .nav-brand { font-size: 0.9rem; }
            .nav-link { padding: 0.3rem 0.5rem; font-size: 0.7rem; }
            .trend-metrics { grid-template-columns: repeat(3, 1fr); gap: 2px; }
            .trend-score { font-size: 1rem; }
            .trend-name { font-size: 0.9rem; }
            .metric-value { font-size: 0.8rem; }
            .metric-label { font-size: 0.65rem; }
            .page-header h1 { font-size: 1rem; }
            .page-header p { font-size: 0.8rem; }
            #dashboard .trends-grid { gap: 0.5rem; }
        }
'''
content = content.replace('</style>', responsive_css + '</style>')

# Make local/international containers stack on mobile by adding class to the wrapping grid
# The dashboard local/international grid is inside a div with inline style display:grid;grid-template-columns:1fr 1fr; we need to add class or adjust inline style to be responsive.
# We'll replace the inline style with a class that we style in media query.
content = content.replace('<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2rem;">',
                          '<div class="location-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2rem;">')

# Add style for .location-grid in responsive CSS
responsive_css2 = '''
        .location-grid { grid-template-columns: 1fr 1fr; }
        @media (max-width: 768px) {
            .location-grid { grid-template-columns: 1fr; }
        }
'''
content = content.replace('</style>', responsive_css2 + '</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Mobile-friendly styles added")
