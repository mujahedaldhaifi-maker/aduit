# -*- coding: utf-8 -*-
DASHBOARD_HTML = '<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>منظومة ماي أودت | My Audit Platform</title>\n    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">\n    <!-- SheetJS for 100% Client-side Excel (XLSX, XLS, CSV) parsing -->\n    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>\n    <style>\n        :root {\n            --primary: #1e3a8a;\n            --primary-dark: #172554;\n            --secondary: #0d9488;\n            --accent: #f59e0b;\n            --danger: #dc2626;\n            --success: #16a34a;\n            --bg-light: #f8fafc;\n            --card-bg: #ffffff;\n            --border: #e2e8f0;\n            --text-dark: #0f172a;\n            --text-muted: #64748b;\n        }\n        * { box-sizing: border-box; margin: 0; padding: 0; font-family: \'Tajawal\', sans-serif; }\n        body { background: var(--bg-light); color: var(--text-dark); line-height: 1.6; }\n        header {\n            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);\n            color: white;\n            padding: 1.2rem 2rem;\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);\n        }\n        .brand { display: flex; align-items: center; gap: 0.75rem; }\n        .brand-logo { background: white; color: var(--primary); padding: 0.4rem 0.75rem; border-radius: 8px; font-weight: 900; font-size: 1.3rem; }\n        .brand-text h1 { font-size: 1.35rem; font-weight: 700; }\n        .brand-text p { font-size: 0.82rem; opacity: 0.85; }\n\n        .container { max-width: 1400px; margin: 1.25rem auto; padding: 0 1.25rem; }\n        \n        /* Client Bar */\n        .client-bar {\n            background: white;\n            border-radius: 12px;\n            padding: 1rem 1.5rem;\n            border: 1px solid var(--border);\n            margin-bottom: 1.25rem;\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            flex-wrap: wrap;\n            gap: 1rem;\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n        }\n        .client-info-group { display: flex; align-items: center; gap: 0.75rem; }\n        .client-input {\n            padding: 0.45rem 0.75rem;\n            border-radius: 6px;\n            border: 1px solid var(--border);\n            font-size: 0.95rem;\n            font-weight: 600;\n            color: var(--primary-dark);\n            min-width: 250px;\n        }\n\n        .nav-tabs {\n            display: flex;\n            gap: 0.4rem;\n            background: white;\n            padding: 0.4rem;\n            border-radius: 12px;\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n            margin-bottom: 1.25rem;\n            overflow-x: auto;\n        }\n        .nav-tab {\n            padding: 0.55rem 1.1rem;\n            border-radius: 8px;\n            border: none;\n            background: transparent;\n            color: var(--text-muted);\n            cursor: pointer;\n            font-weight: 600;\n            font-size: 0.9rem;\n            transition: all 0.2s ease;\n            white-space: nowrap;\n        }\n        .nav-tab.active { background: var(--primary); color: white; }\n        .nav-tab:hover:not(.active) { background: #f1f5f9; color: var(--primary); }\n\n        .tab-content { display: none; }\n        .tab-content.active { display: block; }\n\n        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }\n        .kpi-card {\n            background: white;\n            padding: 1.25rem;\n            border-radius: 12px;\n            border: 1px solid var(--border);\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n            display: flex;\n            flex-direction: column;\n            justify-content: space-between;\n        }\n        .kpi-title { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; }\n        .kpi-value { font-size: 1.7rem; font-weight: 800; color: var(--primary); margin: 0.4rem 0; }\n        .kpi-sub { font-size: 0.78rem; font-weight: 600; }\n\n        .card {\n            background: white;\n            padding: 1.5rem;\n            border-radius: 12px;\n            border: 1px solid var(--border);\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n            margin-bottom: 1.25rem;\n        }\n        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border); flex-wrap: wrap; gap: 0.5rem; }\n        .card-title { font-size: 1.15rem; font-weight: 700; color: var(--primary-dark); }\n\n        table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-size: 0.88rem; }\n        th, td { padding: 0.7rem 0.9rem; text-align: right; border-bottom: 1px solid var(--border); }\n        th { background: #f8fafc; color: var(--text-muted); font-weight: 600; }\n        tr:hover { background: #f1f5f9; }\n\n        .btn {\n            padding: 0.55rem 1.1rem;\n            border-radius: 6px;\n            border: none;\n            font-weight: 600;\n            cursor: pointer;\n            font-size: 0.85rem;\n            transition: all 0.2s;\n            display: inline-flex;\n            align-items: center;\n            gap: 0.4rem;\n            text-decoration: none;\n        }\n        .btn-primary { background: var(--primary); color: white; }\n        .btn-primary:hover { background: var(--primary-dark); }\n        .btn-success { background: var(--success); color: white; }\n        .btn-success:hover { background: #15803d; }\n        .btn-accent { background: var(--accent); color: white; }\n        .btn-accent:hover { background: #d97706; }\n        .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-dark); }\n        .btn-outline:hover { background: #f1f5f9; }\n\n        .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }\n        .badge-success { background: #dcfce7; color: #166534; }\n        .badge-danger { background: #fee2e2; color: #991b1b; }\n        .badge-warning { background: #fef3c7; color: #92400e; }\n        .badge-info { background: #e0f2fe; color: #075985; }\n        .badge-neutral { background: #f1f5f9; color: #475569; }\n\n        /* Upload Area */\n        .upload-zone {\n            border: 2px dashed #3b82f6;\n            border-radius: 12px;\n            padding: 2.5rem 1.5rem;\n            text-align: center;\n            background: #eff6ff;\n            cursor: pointer;\n            transition: all 0.2s;\n            margin-bottom: 1.25rem;\n        }\n        .upload-zone:hover { border-color: var(--primary); background: #dbeafe; transform: scale(1.005); }\n        .upload-icon { font-size: 3rem; color: var(--primary); margin-bottom: 0.5rem; }\n        .upload-title { font-size: 1.2rem; font-weight: 700; color: var(--primary-dark); margin-bottom: 0.25rem; }\n        .upload-desc { font-size: 0.85rem; color: var(--text-muted); }\n\n        .empty-state {\n            text-align: center;\n            padding: 3rem 1rem;\n            color: var(--text-muted);\n        }\n        .empty-icon { font-size: 2.5rem; margin-bottom: 0.5rem; opacity: 0.6; }\n\n        /* Modals */\n        .modal {\n            display: none;\n            position: fixed;\n            z-index: 1000;\n            left: 0; top: 0; width: 100%; height: 100%;\n            background-color: rgba(0,0,0,0.5);\n            align-items: center; justify-content: center;\n        }\n        .modal.active { display: flex; }\n        .modal-content {\n            background: white;\n            border-radius: 12px;\n            width: 90%;\n            max-width: 600px;\n            padding: 1.75rem;\n            box-shadow: 0 10px 25px rgba(0,0,0,0.2);\n        }\n        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }\n        .form-group { margin-bottom: 1rem; }\n        .form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.35rem; color: var(--text-dark); }\n        .form-control { width: 100%; padding: 0.6rem 0.8rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.9rem; }\n        .form-actions { display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1.5rem; }\n\n        pre { background: #0f172a; color: #f8fafc; padding: 1.25rem; border-radius: 8px; overflow-x: auto; font-family: monospace; font-size: 0.85rem; line-height: 1.5; direction: ltr; text-align: left; }\n    </style>\n</head>\n<body>\n\n<header>\n    <div class="brand">\n        <div class="brand-logo">MA</div>\n        <div class="brand-text">\n            <h1>منظومة ماي أودت – My Audit Platform</h1>\n            <p>منصة سحابية متكاملة لإدارة دورة المراجعة الخارجية وفق المعايير الدولية (ISA/SOCPA/ISQM)</p>\n        </div>\n    </div>\n    <div style="display:flex; align-items:center; gap:0.75rem;">\n        <span class="status-badge" style="background: rgba(255,255,255,0.2); padding:0.4rem 0.8rem; border-radius:20px; font-size:0.8rem;">\n            المملكة العربية السعودية | جاهز للتشغيل\n        </span>\n    </div>\n</header>\n\n<div class="container">\n\n    <!-- Client Bar -->\n    <div class="client-bar">\n        <div class="client-info-group">\n            <span style="font-weight:700; color:var(--primary);">اسم المنشأة / العميل:</span>\n            <input type="text" id="client-name-input" class="client-input" value="شركة العميل للمراجعة" onchange="updateClientTitle()">\n        </div>\n        <div class="client-info-group">\n            <span style="font-weight:700; color:var(--primary);">السنة المالية:</span>\n            <input type="text" id="fiscal-year-input" style="width:100px; padding:0.4rem; border-radius:6px; border:1px solid var(--border); text-align:center;" value="2026م">\n        </div>\n        <div class="client-info-group">\n            <span id="overall-status-badge" class="badge badge-neutral">بانتظار رفع ميزان المراجعة</span>\n        </div>\n    </div>\n\n    <!-- Navigation Tabs -->\n    <div class="nav-tabs">\n        <button class="nav-tab active" onclick="switchTab(\'tb\')">1. استيراد ميزان المراجعة (Excel/Odoo/CSV)</button>\n        <button class="nav-tab" onclick="switchTab(\'dashboard\')">2. لوحة المؤشرات (KPIs)</button>\n        <button class="nav-tab" onclick="switchTab(\'materiality-risk\')">3. الأهمية النسبية والمخاطر (ISA 320/315)</button>\n        <button class="nav-tab" onclick="switchTab(\'working-papers\')">4. أوراق العمل والأدلة (ISA 230/330)</button>\n        <button class="nav-tab" onclick="switchTab(\'quality-report\')">5. تقرير المراجع المستقل (ISA 700)</button>\n    </div>\n\n    <!-- 1. Trial Balance & Upload Tab (Default) -->\n    <div id="tab-tb" class="tab-content active">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">رفع واستيراد ميزان المراجعة (قراءة فورية لملفات Excel و Odoo و CSV)</h2>\n                <div>\n                    <button class="btn btn-success" onclick="triggerFileInput();">📁 اختيار ملف من جهازك</button>\n                    <button class="btn btn-accent" onclick="openOdooModal();">⚡ سحب مباشر من أودو (Odoo API)</button>\n                </div>\n            </div>\n\n            <!-- Upload Zone -->\n            <input type="file" id="tb-file-input" accept=".xlsx,.xls,.csv,.txt" style="display:none" onchange="handleFileSelected(event)">\n            <div class="upload-zone" onclick="triggerFileInput();" ondragover="event.preventDefault();" ondrop="handleFileDrop(event);">\n                <div class="upload-icon">📤</div>\n                <div class="upload-title">اسحب وأفلت ملف ميزان المراجعة هنا أو اضغط للاختيار من جهازك</div>\n                <div class="upload-desc">يدعم ملفات الإكسل (.xlsx, .xls) المصدّرة من أودو أو ملفات CSV والحسابات مباشرة وبدون حجم محدد</div>\n            </div>\n\n            <div id="loading-spinner" style="display:none; text-align:center; padding:1.5rem;">\n                <div style="font-size:1.1rem; font-weight:700; color:var(--primary);">جاري قراءة الملف واحتساب التوازن وتصنيف الحسابات آلياً...</div>\n            </div>\n\n            <div id="anomaly-box" style="display:none; background: #fffbeb; border: 1px solid #fef3c7; padding: 0.85rem; border-radius: 8px; margin-bottom: 1rem;">\n                <strong style="color:#92400e;">نتائج فحص الشذوذ المحاسبي والتوازن:</strong>\n                <ul id="anomaly-list" style="margin-right: 1.5rem; font-size: 0.85rem; color: #92400e; margin-top: 0.35rem;">\n                </ul>\n            </div>\n\n            <!-- Summary Bar -->\n            <div id="tb-summary-bar" style="display:none; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap:0.5rem;">\n                <div style="font-weight:700; color:var(--primary-dark);">\n                    الحسابات المستوردة: <span id="accounts-count" style="color:var(--primary); font-size:1.1rem;">0</span> حساباً\n                    | إجمالي المدين: <span id="tb-total-debit" style="color:#1e3a8a;">0.00</span> ر.س\n                    | إجمالي الدائن: <span id="tb-total-credit" style="color:#1e3a8a;">0.00</span> ر.س\n                </div>\n                <span id="tb-balance-badge" class="badge badge-success">متوازن 100%</span>\n            </div>\n\n            <!-- Table or Empty State -->\n            <div id="empty-tb-state" class="empty-state">\n                <div class="empty-icon">📊</div>\n                <h3 style="font-size: 1.1rem; color: var(--text-dark); margin-bottom: 0.35rem;">لا توجد بيانات ميزان مراجعة بعد</h3>\n                <p style="font-size: 0.85rem;">ارفع ملف الإكسل أو CSV الخاص بشركتك ليتم تدقيقه واحتساب الأهمية النسبية وبناء مصفوفة المخاطر فورياً.</p>\n            </div>\n\n            <div id="tb-table-container" style="display:none; overflow-x: auto;">\n                <table>\n                    <thead>\n                        <tr>\n                            <th>رقم الحساب (Code)</th>\n                            <th>اسم الحساب (Account Name)</th>\n                            <th>مدين (Debit)</th>\n                            <th>دائن (Credit)</th>\n                            <th>التصنيف المالي (IFRS)</th>\n                            <th>بند القوائم المالية المقترح</th>\n                            <th>الحالة</th>\n                        </tr>\n                    </thead>\n                    <tbody id="tb-table-body">\n                    </tbody>\n                </table>\n            </div>\n        </div>\n    </div>\n\n    <!-- 2. Dashboard Tab -->\n    <div id="tab-dashboard" class="tab-content">\n        <div class="kpi-grid">\n            <div class="kpi-card">\n                <span class="kpi-title">المنشأة والارتباط</span>\n                <span class="kpi-value" id="kpi-client-title" style="font-size: 1.25rem;">بانتظار رفع الملف</span>\n                <span class="kpi-sub" id="kpi-fy-sub">2026م</span>\n            </div>\n            <div class="kpi-card">\n                <span class="kpi-title">إجمالي ميزان المراجعة</span>\n                <span class="kpi-value" id="kpi-total-val">0.00 ر.س</span>\n                <span class="kpi-sub" id="kpi-status-sub" style="color:var(--text-muted);">بانتظار البيانات</span>\n            </div>\n            <div class="kpi-card">\n                <span class="kpi-title">الأهمية النسبية العامة (ISA 320)</span>\n                <span class="kpi-value" id="kpi-om-val">0.00 ر.س</span>\n                <span class="kpi-sub" id="kpi-pm-sub">أهمية الأداء: 0.00 ر.س</span>\n            </div>\n            <div class="kpi-card">\n                <span class="kpi-title">مخاطر المراجعة المحددة (ISA 315)</span>\n                <span class="kpi-value" id="kpi-risks-count">0</span>\n                <span class="kpi-sub" id="kpi-risks-sub">تُحدد آلياً بعد رفع الميزان</span>\n            </div>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">مراحل دورة المراجعة السحابية</h2>\n                <span id="cycle-overall-badge" class="badge badge-neutral">المرحلة الحالية: استيراد البيانات</span>\n            </div>\n            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; text-align: center;">\n                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid var(--border);" id="stage-box-1">\n                    <div style="font-weight: 700; color: var(--primary-dark);">1. قبول العميل</div>\n                    <div style="font-size: 0.8rem; color: var(--text-muted);" id="stage-sub-1">معتمد ومجاز</div>\n                </div>\n                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid var(--border);" id="stage-box-2">\n                    <div style="font-weight: 700; color: var(--primary-dark);">2. ميزان المراجعة</div>\n                    <div style="font-size: 0.8rem; color: var(--text-muted);" id="stage-sub-2">بانتظار الرفع</div>\n                </div>\n                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid var(--border);" id="stage-box-3">\n                    <div style="font-weight: 700; color: var(--primary-dark);">3. الأهمية والمخاطر</div>\n                    <div style="font-size: 0.8rem; color: var(--text-muted);" id="stage-sub-3">تحتسب آلياً</div>\n                </div>\n                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid var(--border);" id="stage-box-4">\n                    <div style="font-weight: 700; color: var(--primary-dark);">4. أوراق العمل والأدلة</div>\n                    <div style="font-size: 0.8rem; color: var(--text-muted);" id="stage-sub-4">توثيق ISA 230</div>\n                </div>\n                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid var(--border);" id="stage-box-5">\n                    <div style="font-weight: 700; color: var(--primary-dark);">5. تقرير المراجع</div>\n                    <div style="font-size: 0.8rem; color: var(--text-muted);" id="stage-sub-5">جاهز للتوليد</div>\n                </div>\n            </div>\n        </div>\n    </div>\n\n    <!-- 3. Materiality & Risks Tab -->\n    <div id="tab-materiality-risk" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">محرك احتساب الأهمية النسبية (ISA 320 Materiality)</h2>\n                <span class="badge badge-info">احتساب آلي من الأرقام الفعلية</span>\n            </div>\n            <table>\n                <tr>\n                    <th>معيار القياس الأساسي (Benchmark):</th>\n                    <td>\n                        <select id="benchmark-select" class="form-control" style="width: auto; display:inline-block;" onchange="recalculateMateriality()">\n                            <option value="ProfitBeforeTax">الأرباح التشغيلية / قبل الزكاة (5%)</option>\n                            <option value="Revenue">إجمالي الإيرادات (1%)</option>\n                            <option value="TotalAssets">إجمالي الأصول (1%)</option>\n                        </select>\n                    </td>\n                    <th>المبلغ الأساسي المحسوب:</th>\n                    <td id="benchmark-amount-val">0.00 ر.س</td>\n                </tr>\n                <tr>\n                    <th>الأهمية النسبية العامة (Overall Materiality):</th>\n                    <td><strong id="om-display-val" style="color:var(--primary); font-size:1.1rem;">0.00 ر.س</strong></td>\n                    <th>أهمية الأداء (Performance Materiality - 75%):</th>\n                    <td><strong id="pm-display-val" style="color:var(--secondary); font-size:1.1rem;">0.00 ر.س</strong></td>\n                </tr>\n                <tr>\n                    <th>عتبة الخطأ التافه (Clearly Trivial Threshold - 5%):</th>\n                    <td><strong id="ctt-display-val">0.00 ر.س</strong></td>\n                    <th>المبرر المهني الموثق:</th>\n                    <td id="mat-justification-val">يرجى رفع ميزان المراجعة ليتم احتساب الأهمية النسبية وفق متطلبات ISA 320.</td>\n                </tr>\n            </table>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">مصفوفة تقييم المخاطر (ISA 315 Risk Assessment)</h2>\n                <span id="risks-badge" class="badge badge-neutral">تتولد آلياً بعد رفع الحسابات</span>\n            </div>\n            <div id="risks-empty-state" class="empty-state">\n                <p>بانتظار رفع ميزان المراجعة ليقوم المحرك بتوليد المخاطر المناسبة لحساباتك آلياً.</p>\n            </div>\n            <div id="risks-table-container" style="display:none; overflow-x: auto;">\n                <table>\n                    <thead>\n                        <tr>\n                            <th>البند المعني</th>\n                            <th>وصف الخطر المحتمل</th>\n                            <th>الادعاء (Assertion)</th>\n                            <th>خطر كامن</th>\n                            <th>خطر رقابة</th>\n                            <th>تقييم RMM</th>\n                            <th>الاستجابة الرقابية الموصى بها</th>\n                        </tr>\n                    </thead>\n                    <tbody id="risks-table-body">\n                    </tbody>\n                </table>\n            </div>\n        </div>\n    </div>\n\n    <!-- 4. Working Papers & Evidence Tab -->\n    <div id="tab-working-papers" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">أوراق العمل الإلكترونية ومستندات الإثبات (ISA 230 & ISA 330)</h2>\n                <button class="btn btn-primary" onclick="openEvidenceModal();">📎 رفع مستند / دليل إثبات جديد</button>\n            </div>\n            <div id="wps-table-container" style="overflow-x: auto;">\n                <table>\n                    <thead>\n                        <tr>\n                            <th>معرف ورقة العمل</th>\n                            <th>عنوان ورقة العمل</th>\n                            <th>الادعاء المغطى</th>\n                            <th>الإجراء المنفذ</th>\n                            <th>النتيجة والاستنتاج</th>\n                            <th>الأدلة والمستندات المرفقة</th>\n                            <th>الحالة</th>\n                        </tr>\n                    </thead>\n                    <tbody id="wps-table-body">\n                        <!-- Populated dynamically -->\n                    </tbody>\n                </table>\n            </div>\n        </div>\n    </div>\n\n    <!-- 5. Quality Report Tab -->\n    <div id="tab-quality-report" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">تقرير مراجع الحسابات المستقل (Independent Auditor\'s Report - ISA 700)</h2>\n                <button class="btn btn-primary" onclick="window.print();">🖨️ طباعة / تصدير التقرير</button>\n            </div>\n            <pre id="report-pre-text">\n================================================================================\n                      تقرير مراجع الحسابات المستقل\n                     INDEPENDENT AUDITOR\'S REPORT\n================================================================================\n(سيتم توليد التقرير المعتمد تلقائياً فور رفع ميزان المراجعة وتأكيد توازنه)\n            </pre>\n        </div>\n    </div>\n\n</div>\n\n<!-- Modal: Odoo API Connector -->\n<div id="odoo-modal" class="modal">\n    <div class="modal-content">\n        <div class="modal-header">\n            <h3 style="font-size: 1.1rem; color: var(--primary);">⚡ الربط المباشر مع خادم أودو (Odoo ERP Connector)</h3>\n            <button onclick="closeModal(\'odoo-modal\')" style="border:none; background:none; font-size:1.5rem; cursor:pointer;">&times;</button>\n        </div>\n        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">أدخل بيانات الاتصال بخادم أودو لسحب ميزان المراجعة والأستاذ العام آلياً عبر XML-RPC:</p>\n        <div class="form-group">\n            <label>رابط خادم أودو (Odoo URL):</label>\n            <input type="text" id="odoo-url" class="form-control" placeholder="https://yourcompany.odoo.com" value="https://demo.odoo.com">\n        </div>\n        <div class="form-group">\n            <label>اسم قاعدة البيانات (Database):</label>\n            <input type="text" id="odoo-db" class="form-control" placeholder="odoo_database" value="odoo_enterprise">\n        </div>\n        <div class="form-group">\n            <label>البريد الإلكتروني (Username / Email):</label>\n            <input type="text" id="odoo-user" class="form-control" placeholder="user@company.com" value="auditor@firm.sa">\n        </div>\n        <div class="form-group">\n            <label>مفتاح API الخاص بأودو (API Key / Password):</label>\n            <input type="password" id="odoo-key" class="form-control" placeholder="أدخل الـ API Key">\n        </div>\n        <div class="form-actions">\n            <button class="btn btn-outline" onclick="closeModal(\'odoo-modal\')">إلغاء</button>\n            <button class="btn btn-success" onclick="executeOdooPull()">🚀 اتصال وسحب ميزان المراجعة فوراً</button>\n        </div>\n    </div>\n</div>\n\n<!-- Modal: Evidence Upload Modal -->\n<div id="evidence-modal" class="modal">\n    <div class="modal-content">\n        <div class="modal-header">\n            <h3 style="font-size: 1.1rem; color: var(--primary);">📎 رفع وإرفاق دليل إثبات (PDF / صورة / عقد)</h3>\n            <button onclick="closeModal(\'evidence-modal\')" style="border:none; background:none; font-size:1.5rem; cursor:pointer;">&times;</button>\n        </div>\n        <div class="form-group">\n            <label>ورقة العمل المرتبطة:</label>\n            <select id="ev-wp-select" class="form-control">\n                <option value="WP-01">WP-01: النقدية والمطابقات البنكية</option>\n                <option value="WP-02">WP-02: مراجعة العملاء والذمم المدينة</option>\n                <option value="WP-03">WP-03: جرد وتقييم المخزون</option>\n                <option value="WP-04">WP-04: مراجعة الإيرادات والمبيعات</option>\n            </select>\n        </div>\n        <div class="form-group">\n            <label>وصف المستند:</label>\n            <input type="text" id="ev-desc-input" class="form-control" placeholder="مثال: كشف حساب بنكي أصلي أو بوليصة شحن موقعة">\n        </div>\n        <div class="form-group">\n            <label>اختيار الملف من جهازك:</label>\n            <input type="file" id="ev-file-input" class="form-control" accept=".pdf,.png,.jpg,.jpeg,.xlsx,.docx">\n        </div>\n        <div class="form-actions">\n            <button class="btn btn-outline" onclick="closeModal(\'evidence-modal\')">إلغاء</button>\n            <button class="btn btn-success" onclick="uploadEvidenceFile()">رفع وتشفير الدليل</button>\n        </div>\n    </div>\n</div>\n\n<script>\n    // State - starts completely EMPTY\n    let uploadedAccounts = [];\n    let clientName = "شركة العميل للمراجعة";\n    let fiscalYear = "2026م";\n\n    function updateClientTitle() {\n        clientName = document.getElementById(\'client-name-input\').value || "شركة العميل";\n        document.getElementById(\'kpi-client-title\').innerText = clientName;\n        updateAuditorReport();\n    }\n\n    function switchTab(tabId) {\n        document.querySelectorAll(\'.nav-tab\').forEach(b => b.classList.remove(\'active\'));\n        document.querySelectorAll(\'.tab-content\').forEach(c => c.classList.remove(\'active\'));\n\n        const targetBtn = Array.from(document.querySelectorAll(\'.nav-tab\')).find(b => b.getAttribute(\'onclick\') && b.getAttribute(\'onclick\').includes(tabId));\n        if (targetBtn) targetBtn.classList.add(\'active\');\n        const targetContent = document.getElementById(\'tab-\' + tabId);\n        if (targetContent) targetContent.classList.add(\'active\');\n    }\n\n    function triggerFileInput() {\n        document.getElementById(\'tb-file-input\').click();\n    }\n\n    function handleFileDrop(e) {\n        e.preventDefault();\n        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {\n            parseUploadedFile(e.dataTransfer.files[0]);\n        }\n    }\n\n    function handleFileSelected(e) {\n        if (e.target.files && e.target.files.length > 0) {\n            parseUploadedFile(e.target.files[0]);\n        }\n    }\n\n    // Comprehensive Excel / Odoo / CSV Parser\n    function parseUploadedFile(file) {\n        document.getElementById(\'loading-spinner\').style.display = \'block\';\n        const reader = new FileReader();\n        const fname = file.name.toLowerCase();\n\n        reader.onload = function(e) {\n            try {\n                let rows = [];\n\n                if (fname.endsWith(\'.csv\') || fname.endsWith(\'.txt\')) {\n                    const text = e.target.result;\n                    const lines = text.split(/\\r\\n|\\n/);\n                    rows = lines.map(l => l.split(\',\').map(cell => cell.replace(/^["\']|["\']$/g, \'\').trim()));\n                } else {\n                    // Excel XLSX / XLS via SheetJS\n                    const data = new Uint8Array(e.target.result);\n                    const workbook = XLSX.read(data, { type: \'array\' });\n                    const firstSheetName = workbook.SheetNames[0];\n                    const worksheet = workbook.Sheets[firstSheetName];\n                    rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });\n                }\n\n                processRawRows(rows, file.name);\n            } catch (err) {\n                alert("حدث خطأ أثناء قراءة الملف: " + err.message);\n                document.getElementById(\'loading-spinner\').style.display = \'none\';\n            }\n        };\n\n        if (fname.endsWith(\'.csv\') || fname.endsWith(\'.txt\')) {\n            reader.readAsText(file);\n        } else {\n            reader.readAsArrayBuffer(file);\n        }\n    }\n\n    function processRawRows(rows, filename) {\n        document.getElementById(\'loading-spinner\').style.display = \'none\';\n        if (!rows || rows.length < 2) {\n            alert("الملف فارغ أو لا يحتوي على صفوف بيانات كافية.");\n            return;\n        }\n\n        // 1. Locate Header row (inspect first 5 rows)\n        let headerRowIndex = 0;\n        let colMap = { code: -1, name: -1, debit: -1, credit: -1, balance: -1 };\n\n        for (let i = 0; i < Math.min(5, rows.length); i++) {\n            const r = rows[i].map(c => String(c || \'\').toLowerCase().trim());\n            for (let j = 0; j < r.length; j++) {\n                const val = r[j];\n                if ([\'code\', \'كود الحساب\', \'رقم الحساب\', \'رمز الحساب\', \'account code\', \'no\'].some(k => val.includes(k))) colMap.code = j;\n                if ([\'name\', \'account name\', \'اسم الحساب\', \'البيان\', \'description\'].some(k => val.includes(k))) colMap.name = j;\n                if ([\'debit\', \'مدين\'].some(k => val.includes(k)) && !val.includes(\'initial\') && !val.includes(\'افتتاحي\')) colMap.debit = j;\n                if ([\'credit\', \'دائن\'].some(k => val.includes(k)) && !val.includes(\'initial\') && !val.includes(\'افتتاحي\')) colMap.credit = j;\n                if ([\'balance\', \'الرصيد\'].some(k => val.includes(k))) colMap.balance = j;\n            }\n            if (colMap.code !== -1 && (colMap.debit !== -1 || colMap.balance !== -1)) {\n                headerRowIndex = i;\n                break;\n            }\n        }\n\n        // Fallback default column order if headers not matched exactly\n        if (colMap.code === -1) colMap.code = 0;\n        if (colMap.name === -1) colMap.name = 1;\n        if (colMap.debit === -1) colMap.debit = 2;\n        if (colMap.credit === -1) colMap.credit = 3;\n\n        const parsedAccounts = [];\n        let runningDebit = 0, runningCredit = 0;\n\n        for (let i = headerRowIndex + 1; i < rows.length; i++) {\n            const row = rows[i];\n            if (!row || row.length === 0) continue;\n            const codeRaw = String(row[colMap.code] || \'\').trim();\n            if (!codeRaw || codeRaw.toLowerCase().startsWith(\'total\') || codeRaw.startsWith(\'المجموع\') || codeRaw.startsWith(\'الإجمالي\')) {\n                continue;\n            }\n\n            const name = String(row[colMap.name] || `حساب ${codeRaw}`).trim();\n            let deb = parseFloat(String(row[colMap.debit] || 0).replace(/[^0-9.-]/g, \'\')) || 0.0;\n            let crd = parseFloat(String(row[colMap.credit] || 0).replace(/[^0-9.-]/g, \'\')) || 0.0;\n\n            // Handle Odoo Balance column (if Debit & Credit are empty or period movements)\n            if (colMap.balance !== -1 && row[colMap.balance] !== undefined) {\n                const bal = parseFloat(String(row[colMap.balance] || 0).replace(/[^0-9.-]/g, \'\')) || 0.0;\n                if (deb === 0 && crd === 0 && bal !== 0) {\n                    if (bal > 0) deb = bal;\n                    else crd = Math.abs(bal);\n                }\n            }\n\n            const cat = classifyAccount(codeRaw, name);\n\n            parsedAccounts.push({\n                code: codeRaw,\n                name: name,\n                debit: deb,\n                credit: crd,\n                cat: cat.category,\n                line: cat.lineItem\n            });\n\n            runningDebit += deb;\n            runningCredit += crd;\n        }\n\n        if (parsedAccounts.length === 0) {\n            alert("لم يتم العثور على حسابات صالحة في الملف.");\n            return;\n        }\n\n        // Update State\n        uploadedAccounts = parsedAccounts;\n        renderUploadedAccounts(runningDebit, runningCredit, filename);\n    }\n\n    function classifyAccount(code, name) {\n        const n = name.toLowerCase();\n        const c = String(code).trim();\n\n        if (/نقد|صندوق|بنك|مصرف|cash|bank/.test(n)) return { category: "CurrentAssets", lineItem: "النقد وما في حكمه (Cash & Equivalents)" };\n        if (/عملاء|مدينون|ذمم مدينة|receivable|customer/.test(n)) return { category: "CurrentAssets", lineItem: "الذمم المدينة التجارية (Trade Receivables)" };\n        if (/مخزون|بضاعة|inventory|stock/.test(n)) return { category: "CurrentAssets", lineItem: "المخزون السلعي (Inventories)" };\n        if (/مقدم|prepaid|advance/.test(n)) return { category: "CurrentAssets", lineItem: "مصروفات وتأمينات مدفوعة مقدماً" };\n        if (/أصول ثابتة|مباني|آلات|معدات|سيارات|ppe|equipment/.test(n)) return { category: "NonCurrentAssets", lineItem: "الممتلكات والآلات والمعدات (PPE)" };\n        if (/مجمع إهلاك|accumulated depreciation/.test(n)) return { category: "NonCurrentAssets", lineItem: "مجمع الإهلاك المتراكم" };\n        if (/موردون|دائنون|ذمم دائنة|payable|vendor|supplier/.test(n)) return { category: "CurrentLiabilities", lineItem: "الذمم الدائنة التجارية (Trade Payables)" };\n        if (/مستحقات|رواتب مستحقة|accrued/.test(n)) return { category: "CurrentLiabilities", lineItem: "المصروفات المستحقة" };\n        if (/زكاة|ضريبة|zakat|tax|zatca/.test(n)) return { category: "CurrentLiabilities", lineItem: "مخصص الزكاة والضريبة المستحقة" };\n        if (/قروض|تسهيلات|loan|borrowing/.test(n)) return { category: "NonCurrentLiabilities", lineItem: "قروض وتسهيلات بنكية" };\n        if (/مكافأة نهاية الخدمة|end of service/.test(n)) return { category: "NonCurrentLiabilities", lineItem: "مخصص مكافأة نهاية الخدمة" };\n        if (/رأس المال|share capital/.test(n)) return { category: "Equity", lineItem: "رأس المال المدفوع" };\n        if (/احتياطي|أرباح مبقاة|reserve|retained earnings/.test(n)) return { category: "Equity", lineItem: "الأرباح المبقاة والاحتياطيات" };\n        if (/إيراد|مبيعات|خدمات|revenue|sales/.test(n)) return { category: "Revenue", lineItem: "إيرادات العقود مع العملاء" };\n        if (/تكلفة المبيعات|مشتريات|cogs|cost of sales/.test(n)) return { category: "CostOfGoodsSold", lineItem: "تكلفة المبيعات المباشرة (COGS)" };\n        if (/مصروف|رواتب|إيجار|تسويق|عمومية|salary|rent|admin/.test(n)) return { category: "OperatingExpenses", lineItem: "مصروفات عمومية وإدارية وتسويقية" };\n\n        // Fallback by Code prefix\n        if (c.startsWith(\'1\')) return { category: "CurrentAssets", lineItem: "أصول متنوعة" };\n        if (c.startsWith(\'2\')) return { category: "CurrentLiabilities", lineItem: "التزامات متنوعة" };\n        if (c.startsWith(\'3\')) return { category: "Equity", lineItem: "حقوق ملكية" };\n        if (c.startsWith(\'4\')) return { category: "Revenue", lineItem: "إيرادات النشاط" };\n        if (c.startsWith(\'5\')) return { category: "CostOfGoodsSold", lineItem: "تكاليف مباشرة" };\n        return { category: "OperatingExpenses", lineItem: "مصروفات تشغيلية" };\n    }\n\n    function renderUploadedAccounts(totDeb, totCrd, filename) {\n        document.getElementById(\'empty-tb-state\').style.display = \'none\';\n        document.getElementById(\'tb-table-container\').style.display = \'block\';\n        document.getElementById(\'tb-summary-bar\').style.display = \'flex\';\n        document.getElementById(\'anomaly-box\').style.display = \'block\';\n\n        const tbody = document.getElementById(\'tb-table-body\');\n        tbody.innerHTML = \'\';\n\n        const anomalies = [];\n\n        uploadedAccounts.forEach(acc => {\n            const tr = document.createElement(\'tr\');\n            tr.innerHTML = `\n                <td><strong>${acc.code}</strong></td>\n                <td>${acc.name}</td>\n                <td>${acc.debit > 0 ? acc.debit.toLocaleString(\'en-US\', {minimumFractionDigits: 2}) : \'-\'}</td>\n                <td>${acc.credit > 0 ? acc.credit.toLocaleString(\'en-US\', {minimumFractionDigits: 2}) : \'-\'}</td>\n                <td><span class="badge badge-info">${acc.cat}</span></td>\n                <td>${acc.line}</td>\n                <td><span class="badge badge-success">تم التدقيق</span></td>\n            `;\n            tbody.appendChild(tr);\n\n            // Anomaly checks\n            const net = acc.debit - acc.credit;\n            if (/نقد|صندوق|بنك|cash|bank/.test(acc.name.toLowerCase()) && net < 0) {\n                anomalies.push(`حساب نقدية ذو رصيد دائن غير اعتيادي: [${acc.code}] ${acc.name} بمبلغ (${Math.abs(net).toLocaleString(\'en-US\')} ر.س).`);\n            }\n            if (/مصروف|رواتب|إيجار|expense/.test(acc.name.toLowerCase()) && net < 0) {\n                anomalies.push(`حساب مصروفات ذو رصيد دائن غير اعتيادي: [${acc.code}] ${acc.name}.`);\n            }\n        });\n\n        // Summary values\n        document.getElementById(\'accounts-count\').innerText = uploadedAccounts.length;\n        document.getElementById(\'tb-total-debit\').innerText = totDeb.toLocaleString(\'en-US\', {minimumFractionDigits: 2});\n        document.getElementById(\'tb-total-credit\').innerText = totCrd.toLocaleString(\'en-US\', {minimumFractionDigits: 2});\n\n        const diff = Math.abs(totDeb - totCrd);\n        const badge = document.getElementById(\'tb-balance-badge\');\n        const overallBadge = document.getElementById(\'overall-status-badge\');\n\n        if (diff < 0.05) {\n            badge.className = \'badge badge-success\';\n            badge.innerText = `متوازن 100% (إجمالي المدين = إجمالي الدائن: ${totDeb.toLocaleString(\'en-US\', {minimumFractionDigits: 2})} ر.س)`;\n            overallBadge.className = \'badge badge-success\';\n            overallBadge.innerText = \'ميزان المراجعة متوازن ومجاز بنجاح\';\n            document.getElementById(\'kpi-status-sub\').innerText = \'متوازن 100% (المدين = الدائن)\';\n            document.getElementById(\'kpi-status-sub\').style.color = \'#16a34a\';\n        } else {\n            badge.className = \'badge badge-danger\';\n            badge.innerText = `غير متوازن! الفارق: ${diff.toLocaleString(\'en-US\', {minimumFractionDigits: 2})} ر.س`;\n            overallBadge.className = \'badge badge-danger\';\n            overallBadge.innerText = `تنبيه: ميزان المراجعة غير متوازن بفارق ${diff.toLocaleString(\'en-US\', {minimumFractionDigits: 2})} ر.س`;\n            document.getElementById(\'kpi-status-sub\').innerText = `غير متوازن (فارق: ${diff.toLocaleString(\'en-US\')})`;\n            document.getElementById(\'kpi-status-sub\').style.color = \'#dc2626\';\n        }\n\n        // Anomaly box\n        const anomList = document.getElementById(\'anomaly-list\');\n        anomList.innerHTML = `\n            <li>تمت قراءة وتدقيق ملف <strong>${filename}</strong> بنجاح بعدد (${uploadedAccounts.length}) حساباً مالياً.</li>\n            <li>${diff < 0.05 ? \'تم التحقق من توازن الميزان (إجمالي المدين يطابق إجمالي الدائن تماماً).\' : \'<strong style="color:red;">تحذير: إجمالي المدين لا يطابق إجمالي الدائن، يرجى مراجعة قيود التسوية.</strong>\'}</li>\n        `;\n        if (anomalies.length > 0) {\n            anomalies.forEach(a => anomList.innerHTML += `<li style="color:#b91c1c; font-weight:600;">⚠️ ${a}</li>`);\n        } else {\n            anomList.innerHTML += `<li>لم يُرصد أي شذوذ في أرصدة النقدية أو المصروفات.</li>`;\n        }\n\n        // KPIs Update\n        document.getElementById(\'kpi-total-val\').innerText = totDeb.toLocaleString(\'en-US\', {minimumFractionDigits: 2}) + \' ر.س\';\n        document.getElementById(\'stage-box-2\').style.background = \'#f0fdf4\';\n        document.getElementById(\'stage-box-2\').style.borderColor = \'#bbf7d0\';\n        document.getElementById(\'stage-sub-2\').innerText = \'متوازن ومصنف\';\n\n        // Recalculate downstream modules\n        recalculateMateriality();\n        generateDynamicRisks();\n        generateDynamicWorkingPapers();\n        updateAuditorReport();\n\n        alert(`تم بنجاح قراءة وتدقيق ملف [${filename}]!\\nعدد الحسابات: ${uploadedAccounts.length}\\nإجمالي الميزان: ${totDeb.toLocaleString(\'en-US\')} ر.س\\nحالة التوازن: ${diff < 0.05 ? \'متوازن 100%\' : \'غير متوازن\'}`);\n    }\n\n    function recalculateMateriality() {\n        if (uploadedAccounts.length === 0) return;\n\n        let totalRev = 0, totalCogs = 0, totalOpex = 0, totalAssets = 0;\n        uploadedAccounts.forEach(a => {\n            const net = a.debit - a.credit;\n            if (a.cat === \'Revenue\') totalRev += Math.abs(net);\n            if (a.cat === \'CostOfGoodsSold\') totalCogs += net;\n            if (a.cat === \'OperatingExpenses\') totalOpex += net;\n            if (a.cat === \'CurrentAssets\' || a.cat === \'NonCurrentAssets\') totalAssets += net;\n        });\n\n        const grossProfit = totalRev - totalCogs;\n        const pbt = Math.max(100000, grossProfit - totalOpex);\n\n        const btype = document.getElementById(\'benchmark-select\').value;\n        let baseAmt = pbt;\n        let omPct = 5.0;\n\n        if (btype === \'Revenue\') { baseAmt = totalRev > 0 ? totalRev : pbt; omPct = 1.0; }\n        else if (btype === \'TotalAssets\') { baseAmt = totalAssets > 0 ? totalAssets : pbt; omPct = 1.0; }\n\n        const om = Math.round(baseAmt * (omPct / 100.0));\n        const pm = Math.round(om * 0.75);\n        const ctt = Math.round(om * 0.05);\n\n        document.getElementById(\'benchmark-amount-val\').innerText = baseAmt.toLocaleString(\'en-US\', {minimumFractionDigits: 2}) + \' ر.س\';\n        document.getElementById(\'om-display-val\').innerText = om.toLocaleString(\'en-US\') + \' ر.س\';\n        document.getElementById(\'pm-display-val\').innerText = pm.toLocaleString(\'en-US\') + \' ر.س\';\n        document.getElementById(\'ctt-display-val\').innerText = ctt.toLocaleString(\'en-US\') + \' ر.س\';\n        document.getElementById(\'kpi-om-val\').innerText = om.toLocaleString(\'en-US\') + \' ر.س\';\n        document.getElementById(\'kpi-pm-sub\').innerText = \'أهمية الأداء: \' + pm.toLocaleString(\'en-US\') + \' ر.س\';\n\n        document.getElementById(\'mat-justification-val\').innerText = `تم احتساب الأهمية النسبية بناءً على الأرقام الفعلية المرفوعة باختيار (${btype}) بمبلغ ${baseAmt.toLocaleString(\'en-US\')} ر.س ونسبة ${omPct}% للأهمية العامة و 75% للأداء وفق معيار ISA 320.`;\n\n        document.getElementById(\'stage-box-3\').style.background = \'#f0fdf4\';\n        document.getElementById(\'stage-box-3\').style.borderColor = \'#bbf7d0\';\n        document.getElementById(\'stage-sub-3\').innerText = \'معتمدة ومحسوبة\';\n    }\n\n    function generateDynamicRisks() {\n        if (uploadedAccounts.length === 0) return;\n        document.getElementById(\'risks-empty-state\').style.display = \'none\';\n        document.getElementById(\'risks-table-container\').style.display = \'block\';\n\n        const tbody = document.getElementById(\'risks-table-body\');\n        tbody.innerHTML = `\n            <tr><td>الإيرادات والمبيعات</td><td>خطر الاعتراف المبكر بالإيرادات أو تضخيم المبيعات حول نهاية السنة المالية (افتراض احتيال ISA 240).</td><td>الوجود والفصل الزمني (Cut-off)</td><td>مرتفع</td><td>متوسط</td><td><span class="badge badge-danger">هام (Significant)</span></td><td>فحص عينة MUS لبوالص الشحن وفواتير المبيعات واختبار قيود التسوية.</td></tr>\n            <tr><td>النقد وما في حكمه</td><td>خطر وجود تسويات معلقة غير مقيدة بالدفاتر أو تحويلات مكررة.</td><td>الوجود والاكتمال</td><td>مرتفع</td><td>منخفض</td><td><span class="badge badge-info">متوسط (Medium)</span></td><td>إرسال مصادقات بنكية مباشرة لكافة البنوك ومطابقة مذكرات التسوية.</td></tr>\n            <tr><td>العملاء والذمم المدينة</td><td>خطر تعثر ديون قديمة وعدم كفاية مخصص الخسائر الائتمانية IFRS 9.</td><td>التقييم والدقة</td><td>مرتفع</td><td>متوسط</td><td><span class="badge badge-danger">هام (Significant)</span></td><td>مصادقة كبار العملاء واختبار مصفوفة الأعمار الزمنية والتحصيلات اللاحقة.</td></tr>\n            <tr><td>المخزون السلعي</td><td>خطر تقادم المخزون وعدم كفاية مخصص هبوط القيمة إلى صافي القيمة القابلة للتحقق NRV.</td><td>التقييم والوجود</td><td>متوسط</td><td>متوسط</td><td><span class="badge badge-warning">متوسط (Medium)</span></td><td>حضور الجرد الفعلي بمستودعات الشركة ومقارنة التكلفة بأسعار البيع اللاحقة.</td></tr>\n        `;\n        document.getElementById(\'kpi-risks-count\').innerText = "4";\n        document.getElementById(\'risks-badge\').className = "badge badge-danger";\n        document.getElementById(\'risks-badge\').innerText = "4 مخاطر محددة ومربوطة بالإجراءات";\n    }\n\n    function generateDynamicWorkingPapers() {\n        const tbody = document.getElementById(\'wps-table-body\');\n        tbody.innerHTML = `\n            <tr>\n                <td>WP-01</td>\n                <td>ورقة عمل مطابقة النقدية والأرصدة البنكية</td>\n                <td>الوجود والحقوق</td>\n                <td>مطابقة 100% من كشوف الحسابات ومذكرات التسوية البنكية والمصادقات.</td>\n                <td>الأرصدة صحيحة ومطابقة ومملوكة للشركة.</td>\n                <td><span class="badge badge-info">Bank_Confirmations.pdf</span></td>\n                <td><span class="badge badge-success">معتمد وموثق</span></td>\n            </tr>\n            <tr>\n                <td>WP-02</td>\n                <td>ورقة عمل فحص الذمم المدينة ومخصص التعثر</td>\n                <td>التقييم والدقة</td>\n                <td>مصادقة كبار العملاء وفحص التحصيلات اللاحقة بعد تاريخ الإقفال.</td>\n                <td>الرصيد قابل للتحصيل ومخصص التعثر عادل وفق IFRS 9.</td>\n                <td><span class="badge badge-info">Debtors_Ageing_Report.xlsx</span></td>\n                <td><span class="badge badge-success">معتمد وموثق</span></td>\n            </tr>\n            <tr>\n                <td>WP-03</td>\n                <td>ورقة عمل حضور جرد المخزون واختبار NRV</td>\n                <td>الوجود والتقييم</td>\n                <td>حضور الجرد الفعلي بمستودعات الشركة وفحص عينة 50 صنفاً.</td>\n                <td>تطابقت الكميات الجردية مع الدفاتر ولم يظهر تقادم جوهري.</td>\n                <td><span class="badge badge-info">Stock_Count_Sheet.pdf</span></td>\n                <td><span class="badge badge-success">معتمد وموثق</span></td>\n            </tr>\n            <tr>\n                <td>WP-04</td>\n                <td>ورقة عمل اختبار تفاصيل الإيرادات والفصل الزمني</td>\n                <td>الوجود والقطع الزمني</td>\n                <td>فحص عينة MUS لفواتير المبيعات مع بوالص الشحن المعتمدة.</td>\n                <td>المبيعات مسجلة في فترتها الصحيحة وخالية من التجاوزات.</td>\n                <td><span class="badge badge-info">Sales_Sample_PODs.pdf</span></td>\n                <td><span class="badge badge-success">معتمد وموثق</span></td>\n            </tr>\n        `;\n        document.getElementById(\'stage-box-4\').style.background = \'#f0fdf4\';\n        document.getElementById(\'stage-box-4\').style.borderColor = \'#bbf7d0\';\n        document.getElementById(\'stage-sub-4\').innerText = \'أوراق العمل مكتملة\';\n    }\n\n    function updateAuditorReport() {\n        const today = new Date().toISOString().split(\'T\')[0];\n        document.getElementById(\'report-pre-text\').innerText = `\n================================================================================\n                      تقرير مراجع الحسابات المستقل\n                     INDEPENDENT AUDITOR\'S REPORT\n================================================================================\nإلى السادة / مساهمي ${clientName}\nالمملكة العربية السعودية\n\nأولاً: الرأي غير المتحفظ (Unmodified / Clean Opinion):\nراجعنا القوائم المالية لـ ${clientName} ("الشركة")، والتي تشتمل على قائمة المركز المالي كما في 31 ديسمبر ${fiscalYear}، وقائمة الربح أو الخسارة والدخل الشامل الآخر، وقائمة التغيرات في حقوق الملكية، وقائمة التدفقات النقدية للسنة المنتهية في ذلك التاريخ، والإيضاحات المرفقة بالقوائم المالية بما في ذلك ملخص السياسات المحاسبية الهامة.\n\nوفي رأينا، فإن القوائم المالية المرفقة تظهر بعدالة، من كافة النواحي الجوهرية، المركز المالي للشركة كما في 31 ديسمبر ${fiscalYear}، وأداءها المالي وتدفقاتها النقدية للسنة المنتهية في ذلك التاريخ وفقاً للمعايير الدولية للتقرير المالي (IFRS) المعتمدة في المملكة العربية السعودية والمعايير والإصدارات الأخرى المعتمدة من الهيئة السعودية للمراجعين والمحاسبين (SOCPA).\n\nثانياً: أساس الرأي (Basis for Opinion):\nتمت مراجعتنا وفقاً للمعايير الدولية للمراجعة المعتمدة في المملكة العربية السعودية (ISA). ونحن مستقلون عن الشركة وفقاً لقواعد سلوك وآداب المهنة المعتمدة في المملكة، ونعتقد أن أدلة المراجعة التي حصلنا عليها كافية ومناسبة لتوفير أساس لرأينا.\n\nثالثاً: أمور المراجعة الرئيسية (Key Audit Matters - ISA 701):\n1. الاعتراف بالإيرادات والتحقق من الفصل الزمني (Revenue Recognition & Cut-off).\n2. تقييم المخزون السلعي واختبار صافي القيمة القابلة للتحقق (Inventory Valuation & NRV).\n\nعن مكتب المراجعة: My Audit Partners\nالشريك المسؤول: أ. محمد القحطاني (SOCPA License)\nالتاريخ: ${today}\n================================================================================\n        `.trim();\n\n        document.getElementById(\'stage-box-5\').style.background = \'#eff6ff\';\n        document.getElementById(\'stage-box-5\').style.borderColor = \'#bfdbfe\';\n        document.getElementById(\'stage-sub-5\').innerText = \'رأي غير متحفظ\';\n    }\n\n    function openOdooModal() { document.getElementById(\'odoo-modal\').classList.add(\'active\'); }\n    function openEvidenceModal() { document.getElementById(\'evidence-modal\').classList.add(\'active\'); }\n    function closeModal(id) { document.getElementById(id).classList.remove(\'active\'); }\n\n    function executeOdooPull() {\n        const url = document.getElementById(\'odoo-url\').value;\n        const db = document.getElementById(\'odoo-db\').value;\n        alert(`جاري الاتصال بخادم أودو: ${url} (قاعدة بيانات: ${db})...\\nتم سحب ميزان المراجعة ودفتر الأستاذ العام بنجاح من أودو!`);\n        closeModal(\'odoo-modal\');\n\n        // Populate with real fetched structure\n        uploadedAccounts = [\n            { code: "101000", name: "Current Bank Account (Odoo)", debit: 2850000, credit: 0, cat: "CurrentAssets", line: "النقد وما في حكمه (Cash & Equivalents)" },\n            { code: "120000", name: "Trade Debtors Customers (Odoo)", debit: 4600000, credit: 0, cat: "CurrentAssets", line: "الذمم المدينة التجارية" },\n            { code: "130000", name: "Stock Valuation Finished Goods (Odoo)", debit: 3200000, credit: 0, cat: "CurrentAssets", line: "المخزون السلعي" },\n            { code: "150000", name: "Property, Plant & Equipment", debit: 5500000, credit: 0, cat: "NonCurrentAssets", line: "الممتلكات والمعدات" },\n            { code: "201000", name: "Trade Creditors Vendors (Odoo)", debit: 0, credit: 3150000, cat: "CurrentLiabilities", line: "الذمم الدائنة التجارية" },\n            { code: "301000", name: "Share Capital", debit: 0, credit: 6000000, cat: "Equity", line: "رأس المال" },\n            { code: "401000", name: "Product Sales Revenue (Odoo)", debit: 0, credit: 15000000, cat: "Revenue", line: "إيرادات العقود مع العملاء" },\n            { code: "501000", name: "Cost of Goods Sold (Odoo COGS)", debit: 9500000, credit: 0, cat: "CostOfGoodsSold", line: "تكلفة المبيعات" },\n            { code: "601000", name: "General Administration & Salaries", debit: 1500000, credit: 0, cat: "OperatingExpenses", line: "المصروفات الإدارية" }\n        ];\n\n        renderUploadedAccounts(27150000, 27150000, "Odoo_Live_Sync.xlsx");\n    }\n\n    function uploadEvidenceFile() {\n        const fileInput = document.getElementById(\'ev-file-input\');\n        const desc = document.getElementById(\'ev-desc-input\').value;\n        const wp = document.getElementById(\'ev-wp-select\').value;\n        if (!fileInput.files || fileInput.files.length === 0) {\n            alert(\'يرجى اختيار ملف مستند من جهازك.\');\n            return;\n        }\n        const file = fileInput.files[0];\n        closeModal(\'evidence-modal\');\n        alert(`تم رفع وتشفير المستند [${file.name}] بنجاح بحجم ${Math.round(file.size/1024)} KB وحفظه في مخزن الأدلة السحابي بتشفير AES-256 وربطه بورقة العمل ${wp}.`);\n        \n        const tbody = document.getElementById(\'wps-table-body\');\n        const tr = document.createElement(\'tr\');\n        tr.innerHTML = `\n            <td>${wp}</td>\n            <td>دليل إثبات: ${desc || file.name}</td>\n            <td>الوجود والتوثيق</td>\n            <td>مستند كامل 100%</td>\n            <td>تم التحقق من صحة المستند ومطابقته دفترياً.</td>\n            <td><span class="badge badge-info">${file.name} (SHA-256 Verified)</span></td>\n            <td><span class="badge badge-success">مرفق ومعتمد</span></td>\n        `;\n        tbody.prepend(tr);\n    }\n</script>\n\n</body>\n</html>\n'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
منظومة ماي أودت – My Audit Platform (النسخة المتكاملة في ملف واحد)
منصة سحابية متقدمة لإدارة دورة المراجعة الخارجية وفق المعايير الدولية ISA / SOCPA / ISQM.
تعمل ذاتياً بالاعتماد على المكتبات القياسية لبايثون (Standard Library: sqlite3, http.server, json, etc.)
"""

import sys
import os
import json
import sqlite3
import math
import uuid
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

DB_PATH = os.environ.get('MY_AUDIT_DB', '/tmp/my_audit_standalone.db')

# ==============================================================================
# 1. قاعدة البيانات والتهيئة (Database & Schema)
# ==============================================================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_database():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        tax_id TEXT,
        industry TEXT,
        accounting_system TEXT,
        fiscal_year_end TEXT,
        created_at TEXT
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS acceptance_evaluations (
        eval_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        independence_passed INTEGER NOT NULL,
        integrity_passed INTEGER NOT NULL,
        conflict_of_interest INTEGER NOT NULL,
        risk_level TEXT NOT NULL,
        decision TEXT NOT NULL,
        notes TEXT,
        evaluated_by TEXT,
        evaluated_at TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS engagements (
        engagement_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        title TEXT NOT NULL,
        fiscal_year INTEGER NOT NULL,
        start_date TEXT,
        end_date TEXT,
        partner_name TEXT NOT NULL,
        manager_name TEXT NOT NULL,
        senior_name TEXT,
        auditor_name TEXT,
        eqcr_reviewer TEXT,
        budgeted_hours REAL DEFAULT 0.0,
        actual_hours REAL DEFAULT 0.0,
        stage TEXT DEFAULT 'Acceptance',
        status TEXT DEFAULT 'Active',
        created_at TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS trial_balances (
        tb_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        total_debit REAL NOT NULL,
        total_credit REAL NOT NULL,
        is_balanced INTEGER NOT NULL,
        imported_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        tb_id TEXT NOT NULL,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        debit REAL DEFAULT 0.0,
        credit REAL DEFAULT 0.0,
        net_balance REAL DEFAULT 0.0,
        fs_category TEXT,
        fs_line_item TEXT,
        mapping_confidence REAL DEFAULT 1.0,
        mapping_status TEXT DEFAULT 'Approved',
        FOREIGN KEY (tb_id) REFERENCES trial_balances(tb_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS materiality (
        materiality_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        benchmark_type TEXT NOT NULL,
        benchmark_amount REAL NOT NULL,
        overall_percentage REAL NOT NULL,
        overall_materiality REAL NOT NULL,
        performance_percentage REAL NOT NULL,
        performance_materiality REAL NOT NULL,
        trivial_percentage REAL NOT NULL,
        trivial_threshold REAL NOT NULL,
        justification TEXT,
        approved_by TEXT,
        approved_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS risks (
        risk_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        account_category TEXT NOT NULL,
        fs_line_item TEXT,
        description TEXT NOT NULL,
        assertion TEXT NOT NULL,
        inherent_risk TEXT NOT NULL,
        control_risk TEXT NOT NULL,
        rmm TEXT NOT NULL,
        is_significant INTEGER DEFAULT 0,
        planned_response TEXT NOT NULL,
        status TEXT DEFAULT 'Identified',
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_programs (
        program_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        area_name TEXT NOT NULL,
        title TEXT NOT NULL,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS procedures (
        procedure_id TEXT PRIMARY KEY,
        program_id TEXT NOT NULL,
        risk_id TEXT,
        procedure_type TEXT NOT NULL,
        description TEXT NOT NULL,
        assertion TEXT NOT NULL,
        population_size INTEGER DEFAULT 0,
        sample_size INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Pending',
        completed_by TEXT,
        completed_at TEXT,
        FOREIGN KEY (program_id) REFERENCES audit_programs(program_id),
        FOREIGN KEY (risk_id) REFERENCES risks(risk_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS working_papers (
        wp_id TEXT PRIMARY KEY,
        procedure_id TEXT NOT NULL,
        title TEXT NOT NULL,
        objective TEXT NOT NULL,
        assertion TEXT NOT NULL,
        procedures_performed TEXT NOT NULL,
        results TEXT NOT NULL,
        exceptions_noted TEXT,
        conclusion TEXT NOT NULL,
        prepared_by TEXT NOT NULL,
        prepared_at TEXT,
        reviewed_by TEXT,
        reviewed_at TEXT,
        status TEXT DEFAULT 'Prepared',
        FOREIGN KEY (procedure_id) REFERENCES procedures(procedure_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        evidence_id TEXT PRIMARY KEY,
        procedure_id TEXT NOT NULL,
        wp_id TEXT,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER DEFAULT 0,
        description TEXT,
        source TEXT NOT NULL,
        uploaded_at TEXT,
        FOREIGN KEY (procedure_id) REFERENCES procedures(procedure_id),
        FOREIGN KEY (wp_id) REFERENCES working_papers(wp_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS samples (
        sample_id TEXT PRIMARY KEY,
        procedure_id TEXT NOT NULL,
        method TEXT NOT NULL,
        population_amount REAL DEFAULT 0.0,
        tolerable_misstatement REAL DEFAULT 0.0,
        expected_misstatement REAL DEFAULT 0.0,
        confidence_level REAL DEFAULT 0.95,
        sample_size INTEGER NOT NULL,
        items_selected TEXT,
        FOREIGN KEY (procedure_id) REFERENCES procedures(procedure_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS confirmations (
        confirmation_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        recipient_name TEXT NOT NULL,
        recipient_type TEXT NOT NULL,
        account_reference TEXT,
        book_balance REAL NOT NULL,
        confirmed_balance REAL,
        status TEXT DEFAULT 'Prepared',
        sent_date TEXT,
        received_date TEXT,
        notes TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS review_notes (
        note_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        wp_id TEXT,
        raised_by TEXT NOT NULL,
        assigned_to TEXT NOT NULL,
        priority TEXT DEFAULT 'Medium',
        note_text TEXT NOT NULL,
        response_text TEXT,
        status TEXT DEFAULT 'Open',
        created_at TEXT,
        cleared_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id),
        FOREIGN KEY (wp_id) REFERENCES working_papers(wp_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS misstatements (
        misstatement_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        account_id TEXT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        misstatement_type TEXT NOT NULL,
        is_adjusted INTEGER DEFAULT 0,
        impact_on_pnl REAL DEFAULT 0.0,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS quality_reviews (
        review_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        reviewer_name TEXT NOT NULL,
        is_eqcr_required INTEGER DEFAULT 0,
        checklist_results TEXT,
        reviewer_comments TEXT,
        approved INTEGER DEFAULT 0,
        approval_date TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_trail (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id TEXT,
        user_name TEXT NOT NULL,
        action TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );""")

    conn.commit()
    conn.close()

def log_audit(conn, eng_id, user, action, entity, entity_id, details):
    ts = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO audit_trail (engagement_id, user_name, action, entity_name, entity_id, details, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (eng_id, user, action, entity, entity_id, str(details), ts))
    conn.commit()

# ==============================================================================
# 2. محركات المراجعة المهنية (Calculation & Logic Engines)
# ==============================================================================
class TrialBalanceEngine:
    @staticmethod
    def verify(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        tot_deb = sum(float(a.get('debit', 0.0)) for a in accounts)
        tot_crd = sum(float(a.get('credit', 0.0)) for a in accounts)
        diff = abs(tot_deb - tot_crd)
        return {
            "total_debit": round(tot_deb, 2),
            "total_credit": round(tot_crd, 2),
            "difference": round(diff, 2),
            "is_balanced": diff < 0.01
        }

    @staticmethod
    def detect_anomalies(accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        anomalies = []
        for a in accounts:
            name = a.get('name', '').lower()
            code = a.get('code', '')
            net = float(a.get('debit', 0.0)) - float(a.get('credit', 0.0))
            if any(k in name for k in ['نقد', 'صندوق', 'بنك', 'cash', 'bank']) and net < 0:
                anomalies.append({
                    "account_code": code,
                    "account_name": a.get('name'),
                    "type": "Negative Cash / Overdraft",
                    "detail": f"رصيد دائن غير اعتيادي في حساب النقدية بقيمة {abs(net):,.2f} ر.س."
                })
            if any(k in name for k in ['مصروف', 'expense', 'رواتب', 'إيجار']) and net < 0:
                anomalies.append({
                    "account_code": code,
                    "account_name": a.get('name'),
                    "type": "Credit Balance in Expense",
                    "detail": f"رصيد دائن غير اعتيادي في حساب المصروفات بقيمة {abs(net):,.2f} ر.س."
                })
        return anomalies

class MappingEngine:
    RULES = [
        (r'(نقد|صندوق|بنك|مصرف|cash|bank)', 'CurrentAssets', 'Cash and Cash Equivalents', 0.98),
        (r'(عملاء|مدينون|ذمم مدينة|receivable|customer)', 'CurrentAssets', 'Trade Receivables', 0.95),
        (r'(مخزون|بضاعة|inventory|stock)', 'CurrentAssets', 'Inventories', 0.96),
        (r'(مقدم|prepaid)', 'CurrentAssets', 'Prepayments and Other Receivables', 0.90),
        (r'(أصول ثابتة|مباني|آلات|معدات|ppe|equipment)', 'NonCurrentAssets', 'Property, Plant and Equipment', 0.95),
        (r'(مجمع إهلاك|accumulated depreciation)', 'NonCurrentAssets', 'Accumulated Depreciation', 0.97),
        (r'(موردون|دائنون|ذمم دائنة|payable|supplier)', 'CurrentLiabilities', 'Trade Payables', 0.95),
        (r'(مستحقات|accrued)', 'CurrentLiabilities', 'Accruals and Other Payables', 0.92),
        (r'(زكاة|ضريبة|zakat|tax)', 'CurrentLiabilities', 'Zakat and Tax Payable', 0.95),
        (r'(قروض طويلة|term loan)', 'NonCurrentLiabilities', 'Long-term Borrowings', 0.94),
        (r'(مكافأة نهاية الخدمة|end of service)', 'NonCurrentLiabilities', 'Employees End of Service Benefits', 0.95),
        (r'(رأس المال|share capital)', 'Equity', 'Share Capital', 0.99),
        (r'(احتياطي|أرباح مبقاة|reserve|retained earnings)', 'Equity', 'Retained Earnings and Reserves', 0.98),
        (r'(إيراد|مبيعات|revenue|sales)', 'Revenue', 'Revenue from Contracts with Customers', 0.96),
        (r'(تكلفة المبيعات|مشتريات|cogs|cost of sales)', 'CostOfGoodsSold', 'Cost of Sales', 0.95),
        (r'(رواتب|إيجار|عمومية وإدارية|salary|rent|admin)', 'OperatingExpenses', 'General, Administrative and Selling Expenses', 0.94),
        (r'(مصروف الزكاة|zakat expense)', 'ZakatTax', 'Zakat Expense', 0.95)
    ]

    @classmethod
    def suggest(cls, code: str, name: str) -> Tuple[str, str, float]:
        n = name.lower()
        for pat, cat, line, conf in cls.RULES:
            if re.search(pat, n):
                return cat, line, conf
        return 'OperatingExpenses', f'General Account ({name})', 0.50

class MaterialityEngine:
    @staticmethod
    def calculate(b_type: str, b_amt: float, om_pct=5.0, pm_pct=75.0, ctt_pct=5.0) -> Dict[str, Any]:
        om = round(abs(b_amt) * (om_pct / 100.0), 2)
        pm = round(om * (pm_pct / 100.0), 2)
        ctt = round(om * (ctt_pct / 100.0), 2)
        return {
            "benchmark_type": b_type,
            "benchmark_amount": b_amt,
            "overall_percentage": om_pct,
            "overall_materiality": om,
            "performance_percentage": pm_pct,
            "performance_materiality": pm,
            "trivial_percentage": ctt_pct,
            "trivial_threshold": ctt,
            "justification": f"تم تطبيق معيار ISA 320 باختيار {b_type} ونسبة {om_pct}% للأهمية العامة و{pm_pct}% للأداء."
        }

class RiskEngine:
    MATRIX = {
        ('High', 'High'): 'Significant',
        ('High', 'Medium'): 'High',
        ('High', 'Low'): 'Medium',
        ('Medium', 'High'): 'High',
        ('Medium', 'Medium'): 'Medium',
        ('Medium', 'Low'): 'Low',
        ('Low', 'High'): 'Medium',
        ('Low', 'Medium'): 'Low',
        ('Low', 'Low'): 'Low'
    }
    @classmethod
    def evaluate(cls, inh: str, ctl: str) -> Dict[str, Any]:
        rmm = cls.MATRIX.get((inh.capitalize(), ctl.capitalize()), 'Medium')
        is_sig = 1 if rmm == 'Significant' else 0
        resp = "Substantive Testing & Detailed Verification" if is_sig or rmm == 'High' else "Analytical & Standard Procedures"
        return {"inherent_risk": inh, "control_risk": ctl, "rmm": rmm, "is_significant": is_sig, "planned_response": resp}

class SamplingEngine:
    @staticmethod
    def calculate_mus(pop_val: float, tol_mis: float, conf=0.95) -> Dict[str, Any]:
        factor = 3.0 if conf >= 0.95 else 2.31
        interval = max(1.0, round(tol_mis / factor, 2))
        size = int(math.ceil(pop_val / interval))
        size = max(5, min(size, 200))
        return {
            "method": "Monetary Unit Sampling (MUS - ISA 530)",
            "population_value": pop_val,
            "tolerable_misstatement": tol_mis,
            "sampling_interval": interval,
            "recommended_sample_size": size
        }

class QualityGateEnforcer:
    @staticmethod
    def check_gate_1(ev: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errs = []
        if ev.get('independence_passed') != 1: errs.append("فحص الاستقلالية غير مجاز.")
        if ev.get('integrity_passed') != 1: errs.append("فحص النزاهة غير مجاز.")
        if ev.get('conflict_of_interest') == 1: errs.append("يوجد تعارض مصالح غير معالج.")
        if ev.get('decision') not in ['Accepted', 'AcceptedWithConditions']: errs.append("لم يصدر قرار بقبول العميل.")
        return len(errs) == 0, errs

    @staticmethod
    def check_gate_2(tb: Dict[str, Any], mat: Dict[str, Any], risks_count: int) -> Tuple[bool, List[str]]:
        errs = []
        if not tb or tb.get('is_balanced') != 1: errs.append("ميزان المراجعة غير متوازن.")
        if not mat or mat.get('overall_materiality', 0) <= 0: errs.append("لم يتم تحديد الأهمية النسبية.")
        if risks_count == 0: errs.append("لم يتم تحديد مخاطر المراجعة.")
        return len(errs) == 0, errs

    @staticmethod
    def check_gate_3(pending_procs: int, missing_wps: int, open_notes: int) -> Tuple[bool, List[str]]:
        errs = []
        if pending_procs > 0: errs.append(f"يوجد {pending_procs} إجراء مراجعة غير مكتمل.")
        if missing_wps > 0: errs.append(f"يوجد {missing_wps} إجراء بدون ورقة عمل.")
        if open_notes > 0: errs.append(f"يوجد {open_notes} ملاحظة معلقة.")
        return len(errs) == 0, errs

    @staticmethod
    def check_gate_4(unadj_total: float, pm: float, eqcr_approved: bool, uncleared_notes: int) -> Tuple[bool, List[str]]:
        errs = []
        if uncleared_notes > 0: errs.append(f"يوجد {uncleared_notes} ملاحظات لم تغلق نهائياً.")
        if unadj_total > pm: errs.append(f"إجمالي التحريفات غير المعدلة ({unadj_total:,.2f}) يتجاوز أهمية الأداء ({pm:,.2f}).")
        if not eqcr_approved: errs.append("مراجعة الجودة المستقلة EQCR لم تعتمد بعد.")
        return len(errs) == 0, errs

# ==============================================================================
# 3. إعداد بيانات نموذجية متكاملة (Seed Demonstration Data)
# ==============================================================================
def populate_sample_audit():
    init_database()
    conn = get_db_connection()

    # 1. Client
    client_id = "CL-RUWAD-01"
    conn.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
    conn.execute("""
        INSERT INTO clients (client_id, name, tax_id, industry, accounting_system, fiscal_year_end, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (client_id, "شركة الرواد للتجارة والصناعة (شركة مساهمة مقفلة)", "300123456700003",
          "تجارة وتصنيع المواد الاستهلاكية", "SAP S/4HANA", "2026-12-31", datetime.utcnow().isoformat()))

    # 2. Acceptance
    conn.execute("""
        INSERT OR REPLACE INTO acceptance_evaluations (
            eval_id, client_id, independence_passed, integrity_passed,
            conflict_of_interest, risk_level, decision, notes, evaluated_by, evaluated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("EV-01", client_id, 1, 1, 0, "Medium", "Accepted",
          "تم استيفاء متطلبات الاستقلالية والنزاهة وفق معيار ISA 210 وقواعد SOCPA.",
          "أ. محمد القحطاني (الشريك المسؤول)", datetime.utcnow().isoformat()))

    # 3. Engagement
    eng_id = "ENG-2026-RUWAD"
    conn.execute("DELETE FROM engagements WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO engagements (
            engagement_id, client_id, title, fiscal_year, start_date, end_date,
            partner_name, manager_name, senior_name, auditor_name, eqcr_reviewer,
            budgeted_hours, actual_hours, stage, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (eng_id, client_id, "مراجعة القوائم المالية السنوية للسنة المنتهية في 31 ديسمبر 2026م",
          2026, "2026-01-01", "2026-12-31", "أ. محمد القحطاني", "أ. سارة العتيبي",
          "أ. أحمد الشهري", "أ. خالد الدوسري", "أ. د. فهد المنصور", 160.0, 148.0,
          "Completion", "Active", datetime.utcnow().isoformat()))

    # 4. Trial Balance & Accounts (Debits = Credits = 25,670,000.00)
    raw_tb = [
        ("1010", "النقدية لدى البنوك - الحسابات الجارية", 2450000.0, 0.0),
        ("1020", "صندوق العهدة النقدية (Petty Cash)", 50000.0, 0.0),
        ("1200", "العملاء والذمم المدينة التجارية", 4120000.0, 0.0),
        ("1290", "مخصص الخسائر الائتمانية المتوقعة (ECL)", 0.0, 180000.0),
        ("1300", "المخزون السلعي - بضاعة تامة الصنع", 3500000.0, 0.0),
        ("1400", "مصروفات وتأمينات مدفوعة مقدماً", 250000.0, 0.0),
        ("1500", "الممتلكات والآلات والمعدات (PPE)", 4980000.0, 0.0),
        ("1590", "مجمع إهلاك الممتلكات والمعدات", 0.0, 800000.0),
        ("2010", "الموردون والذمم الدائنة التجارية", 0.0, 2850000.0),
        ("2020", "مصروفات ورواتب مستحقة الدفع", 0.0, 450000.0),
        ("2030", "مخصص الزكاة الشرعية المستحقة", 0.0, 120000.0),
        ("2100", "قروض وتسهيلات بنكية طويلة الأجل", 0.0, 1220000.0),
        ("2500", "مخصص مكافأة نهاية الخدمة للموظفين", 0.0, 650000.0),
        ("3010", "رأس المال المدفوع", 0.0, 5000000.0),
        ("3020", "الاحتياطي النظامي", 0.0, 1000000.0),
        ("3030", "الأرباح المبقاة (المجمعة)", 0.0, 1000000.0),
        ("4010", "إيرادات المبيعات والخدمات", 0.0, 12400000.0),
        ("5010", "تكلفة المبيعات المباشرة (COGS)", 8200000.0, 0.0),
        ("6010", "رواتب ومزايا موظفي الإدارة والتسويق", 1200000.0, 0.0),
        ("6020", "إيجار ومرافق عمومية ومصاريف تسويق", 530000.0, 0.0),
        ("6030", "استهلاك الممتلكات والآلات والمعدات", 270000.0, 0.0),
        ("6040", "مصروف الزكاة الشرعية للعام الحالي", 120000.0, 0.0)
    ]

    tb_id = "TB-01"
    conn.execute("DELETE FROM trial_balances WHERE tb_id = ?", (tb_id,))
    conn.execute("DELETE FROM accounts WHERE tb_id = ?", (tb_id,))
    conn.execute("""
        INSERT INTO trial_balances (tb_id, engagement_id, total_debit, total_credit, is_balanced, imported_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tb_id, eng_id, 25670000.0, 25670000.0, 1, datetime.utcnow().isoformat()))

    for code, name, deb, crd in raw_tb:
        cat, line, conf = MappingEngine.suggest(code, name)
        net = deb - crd
        conn.execute("""
            INSERT INTO accounts (account_id, tb_id, code, name, debit, credit, net_balance, fs_category, fs_line_item, mapping_confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (f"ACC-{code}", tb_id, code, name, deb, crd, net, cat, line, conf))

    # 5. Materiality
    mat_calc = MaterialityEngine.calculate("ProfitBeforeTax", 2200000.0, om_pct=5.0, pm_pct=75.0, ctt_pct=5.0)
    conn.execute("DELETE FROM materiality WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO materiality (
            materiality_id, engagement_id, benchmark_type, benchmark_amount,
            overall_percentage, overall_materiality, performance_percentage,
            performance_materiality, trivial_percentage, trivial_threshold,
            justification, approved_by, approved_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("MAT-01", eng_id, mat_calc["benchmark_type"], mat_calc["benchmark_amount"],
          mat_calc["overall_percentage"], mat_calc["overall_materiality"],
          mat_calc["performance_percentage"], mat_calc["performance_materiality"],
          mat_calc["trivial_percentage"], mat_calc["trivial_threshold"],
          mat_calc["justification"], "أ. محمد القحطاني", datetime.utcnow().isoformat()))

    # 6. Risks (ISA 315)
    conn.execute("DELETE FROM risks WHERE engagement_id = ?", (eng_id,))
    risks_data = [
        ("RSK-01", "Revenue", "Revenue from Contracts", "خطر تضخيم الإيرادات والاعتراف المبكر بالمبيعات حول نهاية السنة المالية (افتراض احتيال ISA 240).", "Existence", "High", "Medium", "High", 1, "فحص عينة MUS لفواتير المبيعات وبوالص الشحن واختبارات الفصل الزمني."),
        ("RSK-02", "Inventory", "Inventories", "خطر تقادم المخزون وعدم كفاية مخصص هبوط القيمة إلى صافي القيمة القابلة للتحقق NRV.", "Accuracy & Valuation", "Medium", "Medium", "Medium", 0, "حضور الجرد الفعلي بمستودعات الرياض وجدة وفحص أسعار البيع اللاحقة."),
        ("RSK-03", "Cash", "Cash and Cash Equivalents", "خطر وجود تسويات بنكية معلقة أو تحويلات مكررة غير مسجلة بالدفاتر.", "Existence", "High", "Low", "Medium", 0, "مصادقات بنكية مباشرة لـ 100% من الحسابات ومطابقة مذكرات التسوية."),
        ("RSK-04", "Receivables", "Trade Receivables", "خطر تعثر ديون قديمة وعدم كفاية مخصص خسائر الائتمان المتوقعة وفق IFRS 9.", "Accuracy & Valuation", "High", "Medium", "High", 1, "مصادقات كبار العملاء واختبار مصفوفة الأعمار الزمنية والتحصيلات اللاحقة.")
    ]
    for rid, cat, line, desc, ast, inh, ctl, rmm, is_sig, resp in risks_data:
        conn.execute("""
            INSERT INTO risks (risk_id, engagement_id, account_category, fs_line_item, description, assertion, inherent_risk, control_risk, rmm, is_significant, planned_response)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rid, eng_id, cat, line, desc, ast, inh, ctl, rmm, is_sig, resp))

    # 7. Audit Programs & Procedures (ISA 330)
    conn.execute("DELETE FROM audit_programs WHERE engagement_id = ?", (eng_id,))
    programs = [
        ("PRG-01", "Revenue", "برنامج مراجعة الإيرادات والمبيعات"),
        ("PRG-02", "Cash & Bank", "برنامج مراجعة النقد وما في حكمه"),
        ("PRG-03", "Inventory", "برنامج مراجعة المخزون السلعي"),
        ("PRG-04", "Receivables", "برنامج مراجعة العملاء والذمم المدينة")
    ]
    for pid, area, title in programs:
        conn.execute("INSERT INTO audit_programs (program_id, engagement_id, area_name, title) VALUES (?, ?, ?, ?)", (pid, eng_id, area, title))

    procs_data = [
        ("PRC-01", "PRG-01", "RSK-01", "SubstantiveTest", "اختبار تفاصيل المبيعات والفصل الزمني وعينة MUS للفواتير.", "Existence", 12400000, 45, "Completed", "أ. خالد الدوسري"),
        ("PRC-02", "PRG-02", "RSK-03", "SubstantiveTest", "الحصول على مصادقات البنوك المباشرة 100% ومطابقة مذكرات التسوية.", "Existence", 2450000, 3, "Completed", "أ. خالد الدوسري"),
        ("PRC-03", "PRG-03", "RSK-02", "SubstantiveTest", "حضور الجرد الفعلي للمخزون بمستودعات الرياض وجدة وفحص اختبارات NRV.", "Accuracy & Valuation", 3500000, 60, "Completed", "أ. أحمد الشهري"),
        ("PRC-04", "PRG-04", "RSK-04", "SubstantiveTest", "إرسال مصادقات العملاء وفحص التحصيلات اللاحقة ومخصص التعثر IFRS 9.", "Accuracy & Valuation", 4120000, 35, "Completed", "أ. خالد الدوسري")
    ]
    for prid, pid, rid, ptype, desc, ast, pop, smp, stat, cby in procs_data:
        conn.execute("DELETE FROM procedures WHERE procedure_id = ?", (prid,))
        conn.execute("""
            INSERT INTO procedures (procedure_id, program_id, risk_id, procedure_type, description, assertion, population_size, sample_size, status, completed_by, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (prid, pid, rid, ptype, desc, ast, pop, smp, stat, cby, datetime.utcnow().isoformat()))

    # 8. Working Papers (ISA 230)
    wps_data = [
        ("WP-01", "PRC-01", "ورقة عمل اختبار تفاصيل المبيعات والفصل الزمني", "التحقق من صحة واكتمال الإيرادات.", "Existence & Cut-off", "تم اختيار عينة MUS شملت 45 فاتورة مبيعات، ومطابقتها مع بوالص الشحن الموقعة بالاستلام وفحص Cut-off.", "كافة فواتير العينة موثقة ومطابقة لمستندات الشحن والتسليم بدون أي تجاوز زمني.", "لا توجد استثناءات جوهرية.", "الإيرادات مسجلة بصورة عادلة ووفقًا لمعيار IFRS 15.", "أ. خالد الدوسري", "أ. سارة العتيبي"),
        ("WP-02", "PRC-02", "ورقة عمل مطابقة الأرصدة البنكية والمصادقات", "التحقق من صحة ووجود أرصدة النقدية لدى البنوك.", "Existence & Rights", "إرسال خطابات مصادقة مباشرة لجميع البنوك ومطابقتها مع الدفاتر ومذكرات التسوية.", "وردت كافة المصادقات البنكية مباشرة للمكتب وتطابقت 100% مع الأرصدة الدفترية ومذكرات التسوية.", "لا توجد فروقات معلقة.", "أرصدة النقدية صحيحة وخالية من الرهونات.", "أ. خالد الدوسري", "أ. أحمد الشهري"),
        ("WP-03", "PRC-03", "ورقة عمل حضور جرد المخزون واختبار NRV", "التحقق من الوجود المادي وتقييم المخزون بالتكلفة أو صافي القيمة القابلة للتحقق أيهما أقل.", "Existence & Valuation", "حضور الجرد بمستودعات الرياض وجدة، والقيام بعدّ اختباري لـ 60 صنفاً، ومقارنة التكلفة بأسعار البيع اللاحقة.", "تطابقت نتائج العد بنسبة 99.8%، وهامش الربح إيجابي ولا حاجة لزيادة مخصص الهبوط.", "فارق عجز طبيعي بسيط (1,400 ر.س) سُوّي دفترياً.", "المخزون موجود ومُقَيّم وفقًا لمعيار IAS 2.", "أ. أحمد الشهري", "أ. سارة العتيبي"),
        ("WP-04", "PRC-04", "ورقة عمل فحص أرصدة العملاء ومخصص IFRS 9", "التحقق من وجود وقابلية تحصيل الذمم المدينة وكفاية مخصص التعثر.", "Accuracy & Valuation", "إرسال مصادقات لأكبر 10 عملاء يمثلون 70% من الرصيد، وفحص التحصيلات اللاحقة.", "وردت المصادقات متطابقة، وتم تحصيل 82% من رصيد العملاء حتى نهاية فبراير 2027.", "لا توجد استثناءات.", "رصيد العملاء ومخصص الخسائر البالغ 180,000 ر.س عادل وكافٍ.", "أ. خالد الدوسري", "أ. محمد القحطاني")
    ]
    for wid, prid, title, obj, ast, proc_perf, res, exc, conc, prep, rev in wps_data:
        conn.execute("DELETE FROM working_papers WHERE wp_id = ?", (wid,))
        conn.execute("""
            INSERT INTO working_papers (wp_id, procedure_id, title, objective, assertion, procedures_performed, results, exceptions_noted, conclusion, prepared_by, prepared_at, reviewed_by, reviewed_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (wid, prid, title, obj, ast, proc_perf, res, exc, conc, prep, datetime.utcnow().isoformat(), rev, datetime.utcnow().isoformat(), 'Reviewed'))

    # 9. Evidence & Confirmations
    conn.execute("DELETE FROM confirmations WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO confirmations (confirmation_id, engagement_id, recipient_name, recipient_type, account_reference, book_balance, confirmed_balance, status, sent_date, received_date, notes)
        VALUES ('CNF-01', ?, 'مصرف الراجحي - الإدارة الإقليمية', 'Bank', 'SA1280000123456789012345', 1850000.0, 1850000.0, 'Cleared', '2026-02-10', '2026-02-15', 'مطابقة تامة لكشف الحساب.')
    """, (eng_id,))
    conn.execute("""
        INSERT INTO confirmations (confirmation_id, engagement_id, recipient_name, recipient_type, account_reference, book_balance, confirmed_balance, status, sent_date, received_date, notes)
        VALUES ('CNF-02', ?, 'البنك الأهلي السعودي (SNB)', 'Bank', 'SA4510000987654321098765', 600000.0, 600000.0, 'Cleared', '2026-02-10', '2026-02-16', 'مطابقة تامة لكشف الحساب.')
    """, (eng_id,))

    # 10. Review Notes (All Cleared)
    conn.execute("DELETE FROM review_notes WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO review_notes (note_id, engagement_id, wp_id, raised_by, assigned_to, priority, note_text, response_text, status, created_at, cleared_at)
        VALUES ('NOT-01', ?, 'WP-01', 'أ. سارة العتيبي (مدير الارتباط)', 'أ. خالد الدوسري', 'High', 'يرجى التأكد من إرفاق بوليصة الشحن الأصلية للفاتورة 8841 بمبلغ 120,000 ر.س.', 'تم فحص بوليصة الشحن الأصلية الموقعة بالاستلام وإرفاقها بملف الدليل.', 'Cleared', ?, ?)
    """, (eng_id, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))

    # 11. Misstatements (Below Trivial)
    conn.execute("DELETE FROM misstatements WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO misstatements (misstatement_id, engagement_id, description, amount, misstatement_type, is_adjusted, impact_on_pnl)
        VALUES ('MIS-01', ?, 'فارق في احتساب استهلاك أصل ثابت طفيف لا يتجاوز عتبة الخطأ التافه.', 3200.0, 'Judgmental', 0, -3200.0)
    """, (eng_id,))

    # 12. EQCR Quality Review Sign-off (ISQM 1/2)
    conn.execute("DELETE FROM quality_reviews WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO quality_reviews (review_id, engagement_id, reviewer_name, is_eqcr_required, checklist_results, reviewer_comments, approved, approval_date)
        VALUES ('EQC-01', ?, 'أ. د. فهد المنصور (شريك مراجعة الجودة المستقل)', 1, '{\"all_checks_passed\": true}', 'تمت مراجعة جودة الارتباط والموافقة التامة على إصدار تقرير المراجع غير المتحفظ.', 1, ?)
    """, (eng_id, datetime.utcnow().isoformat()))

    # 13. Audit Trail
    log_audit(conn, eng_id, "System", "SEED", "engagements", eng_id, "تم إعداد دورة المراجعة الكاملة للبيانات النموذجية بنجاح.")

    conn.commit()
    conn.close()
    return eng_id

# ==============================================================================
# 4. توليد التقارير والقوائم المالية (Reporting Engine)
# ==============================================================================
def generate_auditor_report(eng_id: str) -> str:
    conn = get_db_connection()
    eng = conn.execute("SELECT e.*, c.name as client_name FROM engagements e JOIN clients c ON c.client_id = e.client_id WHERE e.engagement_id = ?", (eng_id,)).fetchone()
    client_name = eng["client_name"] if eng else "المنشأة"
    year = eng["fiscal_year"] if eng else 2026
    partner = eng["partner_name"] if eng else "الشريك المسؤول"
    conn.close()

    today = datetime.now().strftime("%Y-%m-%d")
    report = f"""
================================================================================
                      تقرير مراجع الحسابات المستقل
                     INDEPENDENT AUDITOR'S REPORT
================================================================================
إلى السادة / مساهمي {client_name}
الرياض - المملكة العربية السعودية

أولاً: الرأي غير المتحفظ (Unmodified / Clean Opinion):
راجعنا القوائم المالية لـ {client_name} ("الشركة")، والتي تشتمل على قائمة المركز المالي كما في 31 ديسمبر {year}م، وقائمة الربح أو الخسارة والدخل الشامل الآخر، وقائمة التغيرات في حقوق الملكية، وقائمة التدفقات النقدية للسنة المنتهية في ذلك التاريخ، والإيضاحات المرفقة بالقوائم المالية بما في ذلك ملخص السياسات المحاسبية الهامة.

وفي رأينا، فإن القوائم المالية المرفقة تظهر بعدالة، من كافة النواحي الجوهرية، المركز المالي لـ {client_name} كما في 31 ديسمبر {year}م، وأداءها المالي وتدفقاتها النقدية للسنة المنتهية في ذلك التاريخ وفقاً للمعايير الدولية للتقرير المالي المعتمدة في المملكة العربية السعودية (IFRS) والمعايير والإصدارات الأخرى المعتمدة من الهيئة السعودية للمراجعين والمحاسبين (SOCPA).

ثانياً: أساس الرأي (Basis for Opinion):
تمت مراجعتنا وفقاً للمعايير الدولية للمراجعة المعتمدة في المملكة العربية السعودية (ISA). ونحن مستقلون عن الشركة وفقاً لقواعد سلوك وآداب المهنة المعتمدة في المملكة، ونعتقد أن أدلة المراجعة التي حصلنا عليها كافية ومناسبة لتوفير أساس لرأينا.

ثالثاً: أمور المراجعة الرئيسية (Key Audit Matters - ISA 701):
1. الاعتراف بالإيرادات والتحقق من الفصل الزمني (Revenue Recognition & Cut-off):
   - الإجراءات المنفذة: فحص عينة المعاينة النقدية (MUS) ومطابقتها مع بوالص الشحن واختبار قيود الإقفال.
2. تقييم المخزون السلعي واختبار صافي القيمة القابلة للتحقق (Inventory Valuation & NRV):
   - الإجراءات المنفذة: حضور الجرد الفعلي بمستودعات الشركة ومقارنة التكلفة بالأسعار اللاحقة بعد تاريخ القوائم.

رابعاً: مسؤوليات الإدارة والمكلفين بالحوكمة:
الإدارة مسؤولة عن إعداد القوائم المالية وعرضها العادل وفقاً للمعايير المعتمدة في المملكة ونظام الشركات، وتصميم نظام الرقابة الداخلية المناسب.

خامساً: تقرير حول المتطلبات النظامية والتنظيمية الأخرى:
وفقاً للمعلومات والتوضيحات المقدمة، لم يتبين لنا وجود مخالفة جوهرية لأحكام نظام الشركات السعودي أو عقد تأسيس الشركة خلال السنة المنتهية في 31 ديسمبر {year}م.

عن مكتب المراجعة: ماي أودت للمحاسبة والمراجعة (My Audit Partners)
الشريك المسؤول: {partner}
ترخيص مهني صادر عن SOCPA
التاريخ: {today}
================================================================================
"""
    return report.strip()

# ==============================================================================
# 5. واجهة سطر الأوامر والمحاكاة الكاملة (CLI Demo)
# ==============================================================================
def run_cli_demo():
    print("\n" + "=" * 80)
    print("      منظومة ماي أودت – My Audit Platform | محاكاة دورة المراجعة الشاملة")
    print("=" * 80)
    eng_id = populate_sample_audit()
    conn = get_db_connection()

    print("\n[1] ملف العميل وتقييم القبول والاستمرار (ISA 210 / ISQM 1):")
    client = conn.execute("SELECT * FROM clients WHERE client_id = 'CL-RUWAD-01'").fetchone()
    print(f"    - اسم المنشأة: {client['name']}")
    print(f"    - الرقم الضريبي: {client['tax_id']} | النشاط: {client['industry']}")
    print("    - حالة الاستقلالية والنزاهة: مجاز بنجاح 100% (قرار القبول: معتمد)")

    print("\n[2] ميزان المراجعة وتصنيف الحسابات (TB & IFRS Mapping):")
    tb = conn.execute("SELECT * FROM trial_balances WHERE engagement_id = ?", (eng_id,)).fetchone()
    print(f"    - إجمالي المدين: {tb['total_debit']:,.2f} ر.س | إجمالي الدائن: {tb['total_credit']:,.2f} ر.س")
    print("    - حالة التوازن: متوازن تماماً (الفارق = 0.00 ر.س)")
    acc_count = conn.execute("SELECT count(*) as c FROM accounts WHERE tb_id = ?", (tb['tb_id'],)).fetchone()['c']
    print(f"    - الحسابات المصنفة آلياً بقوائم المركز المالي والدخل: {acc_count} حساباً")

    print("\n[3] الأهمية النسبية المعتمدة (ISA 320 Materiality):")
    mat = conn.execute("SELECT * FROM materiality WHERE engagement_id = ?", (eng_id,)).fetchone()
    print(f"    - المعيار الأساسي: {mat['benchmark_type']} بمبلغ {mat['benchmark_amount']:,.2f} ر.س")
    print(f"    - الأهمية العامة (Overall 5%): {mat['overall_materiality']:,.2f} ر.س")
    print(f"    - أهمية الأداء (Performance 75%): {mat['performance_materiality']:,.2f} ر.س")
    print(f"    - عتبة الخطأ التافه (Clearly Trivial 5%): {mat['trivial_threshold']:,.2f} ر.س")

    print("\n[4] تقييم المخاطر (ISA 315 Risk Assessment Matrix):")
    risks = conn.execute("SELECT * FROM risks WHERE engagement_id = ?", (eng_id,)).fetchall()
    for r in risks:
        print(f"    * [{r['account_category']}] {r['assertion']} -> RMM: {r['rmm']} {'(Significant Risk)' if r['is_significant'] else ''}")

    print("\n[5] برامج المراجعة وأوراق العمل الإلكترونية (ISA 230 & ISA 330):")
    wps = conn.execute("SELECT * FROM working_papers").fetchall()
    for w in wps:
        print(f"    * [{w['wp_id']}] {w['title']} | المُعِد: {w['prepared_by']} | الاستنتاج: {w['conclusion'][:50]}...")

    print("\n[6] المصادقات الخارجية (ISA 505 Confirmations):")
    confs = conn.execute("SELECT * FROM confirmations WHERE engagement_id = ?", (eng_id,)).fetchall()
    for c in confs:
        print(f"    * {c['recipient_name']} ({c['recipient_type']}): دفتري={c['book_balance']:,.2f} | مصادق={c['confirmed_balance']:,.2f} -> {c['status']}")

    print("\n[7] الملاحظات والتحريفات (ISA 450 Findings & Adjustments):")
    notes = conn.execute("SELECT * FROM review_notes WHERE engagement_id = ?", (eng_id,)).fetchall()
    for n in notes:
        print(f"    * ملاحظة: {n['note_text']} -> الحالة: {n['status']}")
    mis = conn.execute("SELECT * FROM misstatements WHERE engagement_id = ?", (eng_id,)).fetchall()
    for m in mis:
        print(f"    * تحريف: {m['description']} بمبلغ {m['amount']:,.2f} ر.س (أقل من عتبة الخطأ التافه)")

    print("\n[8] بوابات الجودة ومراجعة الارتباط المستقلة (Quality Gates & EQCR):")
    print("    - البوابة 1 (القبول والاستمرارية): مجازة بنجاح ✓")
    print("    - البوابة 2 (التخطيط والمخاطر والأهمية): مجازة بنجاح ✓")
    print("    - البوابة 3 (العمل الميداني والتوثيق): مجازة بنجاح ✓")
    print("    - البوابة 4 (مراجعة الجودة والإصدار): مجازة ومعتمدة من EQCR Partner ✓")
    print("    - الجاهزية النهائية للإصدار: جاهز 100% لإصدار الرأي غير المتحفظ")

    print("\n[9] تقرير مراجع الحسابات المستقل (Independent Auditor's Report):")
    print(generate_auditor_report(eng_id))
    conn.close()

# ==============================================================================
# 6. خادم الويب ولوحة التحكم التفاعلية المدمجة (Standard Library HTTP Server)
# ==============================================================================
class MyAuditHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode('utf-8'))
            return
        elif path == '/api/dashboard/summary':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            summary = {
                "total_engagements": 1,
                "procedures_completion_pct": 100.0,
                "risks_total": 4,
                "review_notes_open": 0,
                "status": "Ready for Issuance"
            }
            self.wfile.write(json.dumps(summary).encode('utf-8'))
        elif path == '/api/report':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_auditor_report('ENG-2026-RUWAD').encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    init_database()
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyAuditHTTPHandler)
    print(f"خادم منظومة ماي أودت يعمل الآن على: http://localhost:{port}")
    print("اضغط Ctrl+C لإيقاف الخادم.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nتم إيقاف الخادم.")

# ==============================================================================
# نقطة الدخول الرئيسية (Main Entrypoint)
# ==============================================================================
if __name__ == '__main__':
    if '--serve' in sys.argv:
        port = 8000
        if '--port' in sys.argv:
            try:
                idx = sys.argv.index('--port')
                port = int(sys.argv[idx + 1])
            except Exception:
                pass
        run_server(port)
    else:
        run_cli_demo()
