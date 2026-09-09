# -*- coding: utf-8 -*-
DASHBOARD_HTML = '<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>منظومة ماي أودت | My Audit Platform</title>\n    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">\n    <style>\n        :root {\n            --primary: #1e3a8a;\n            --primary-dark: #172554;\n            --secondary: #0d9488;\n            --accent: #f59e0b;\n            --danger: #dc2626;\n            --success: #16a34a;\n            --bg-light: #f8fafc;\n            --card-bg: #ffffff;\n            --border: #e2e8f0;\n            --text-dark: #0f172a;\n            --text-muted: #64748b;\n        }\n        * { box-sizing: border-box; margin: 0; padding: 0; font-family: \'Tajawal\', sans-serif; }\n        body { background: var(--bg-light); color: var(--text-dark); line-height: 1.6; }\n        header {\n            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);\n            color: white;\n            padding: 1.25rem 2rem;\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);\n        }\n        .brand { display: flex; align-items: center; gap: 0.75rem; }\n        .brand-logo { background: white; color: var(--primary); padding: 0.5rem 0.75rem; border-radius: 8px; font-weight: 900; font-size: 1.25rem; }\n        .brand-text h1 { font-size: 1.4rem; font-weight: 700; }\n        .brand-text p { font-size: 0.85rem; opacity: 0.85; }\n        .status-badge { background: rgba(255,255,255,0.15); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem; }\n\n        .container { max-width: 1400px; margin: 1.5rem auto; padding: 0 1.5rem; }\n        .nav-tabs {\n            display: flex;\n            gap: 0.5rem;\n            background: white;\n            padding: 0.5rem;\n            border-radius: 12px;\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n            margin-bottom: 1.5rem;\n            overflow-x: auto;\n        }\n        .nav-tab {\n            padding: 0.6rem 1.2rem;\n            border-radius: 8px;\n            border: none;\n            background: transparent;\n            color: var(--text-muted);\n            cursor: pointer;\n            font-weight: 600;\n            font-size: 0.95rem;\n            transition: all 0.2s ease;\n            white-space: nowrap;\n        }\n        .nav-tab.active { background: var(--primary); color: white; }\n        .nav-tab:hover:not(.active) { background: #f1f5f9; color: var(--primary); }\n\n        .tab-content { display: none; }\n        .tab-content.active { display: block; }\n\n        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }\n        .kpi-card {\n            background: white;\n            padding: 1.25rem;\n            border-radius: 12px;\n            border: 1px solid var(--border);\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n            display: flex;\n            flex-direction: column;\n            justify-content: space-between;\n        }\n        .kpi-title { font-size: 0.85rem; color: var(--text-muted); font-weight: 500; }\n        .kpi-value { font-size: 1.8rem; font-weight: 800; color: var(--primary); margin: 0.5rem 0; }\n        .kpi-sub { font-size: 0.75rem; color: var(--secondary); font-weight: 600; }\n\n        .card {\n            background: white;\n            padding: 1.5rem;\n            border-radius: 12px;\n            border: 1px solid var(--border);\n            box-shadow: 0 1px 3px rgba(0,0,0,0.05);\n            margin-bottom: 1.5rem;\n        }\n        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border); }\n        .card-title { font-size: 1.2rem; font-weight: 700; color: var(--primary-dark); }\n\n        table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-size: 0.9rem; }\n        th, td { padding: 0.75rem 1rem; text-align: right; border-bottom: 1px solid var(--border); }\n        th { background: #f8fafc; color: var(--text-muted); font-weight: 600; }\n        tr:hover { background: #f1f5f9; }\n\n        .btn {\n            padding: 0.5rem 1rem;\n            border-radius: 6px;\n            border: none;\n            font-weight: 600;\n            cursor: pointer;\n            font-size: 0.85rem;\n            transition: all 0.2s;\n            display: inline-flex;\n            align-items: center;\n            gap: 0.4rem;\n        }\n        .btn-primary { background: var(--primary); color: white; }\n        .btn-primary:hover { background: var(--primary-dark); }\n        .btn-success { background: var(--success); color: white; }\n        .btn-success:hover { background: #15803d; }\n        .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-dark); }\n        .btn-outline:hover { background: #f1f5f9; }\n\n        .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }\n        .badge-success { background: #dcfce7; color: #166534; }\n        .badge-danger { background: #fee2e2; color: #991b1b; }\n        .badge-warning { background: #fef3c7; color: #92400e; }\n        .badge-info { background: #e0f2fe; color: #075985; }\n\n        .gate-box { display: flex; align-items: center; justify-content: space-between; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; border: 1px solid var(--border); }\n        .gate-passed { background: #f0fdf4; border-color: #bbf7d0; }\n        .gate-failed { background: #fef2f2; border-color: #fecaca; }\n\n        pre { background: #0f172a; color: #f8fafc; padding: 1.25rem; border-radius: 8px; overflow-x: auto; font-family: monospace; font-size: 0.85rem; line-height: 1.5; direction: ltr; text-align: left; }\n    </style>\n</head>\n<body>\n\n<header>\n    <div class="brand">\n        <div class="brand-logo">MA</div>\n        <div class="brand-text">\n            <h1>منظومة ماي أودت – My Audit</h1>\n            <p>المنصة السحابية المتقدمة لإدارة عمليات المراجعة الخارجية وفق المعايير الدولية (ISA/SOCPA/ISQM)</p>\n        </div>\n    </div>\n    <div class="status-badge">\n        <span>المملكة العربية السعودية | معتمدة مهنيًا</span>\n    </div>\n</header>\n\n<div class="container">\n    <div class="nav-tabs">\n        <button class="nav-tab active" onclick="switchTab(\'dashboard\')">لوحة التحكم التنفيذية</button>\n        <button class="nav-tab" onclick="switchTab(\'acceptance\')">قبول العميل والارتباط</button>\n        <button class="nav-tab" onclick="switchTab(\'tb\')">ميزان المراجعة والتصنيف</button>\n        <button class="nav-tab" onclick="switchTab(\'materiality-risk\')">الأهمية النسبية والمخاطر (ISA 315/320)</button>\n        <button class="nav-tab" onclick="switchTab(\'working-papers\')">برامج وأوراق العمل (ISA 230/330)</button>\n        <button class="nav-tab" onclick="switchTab(\'sampling-confirmations\')">العينات والمصادقات (ISA 505/530)</button>\n        <button class="nav-tab" onclick="switchTab(\'review-misstatements\')">الملاحظات والتحريفات (ISA 450)</button>\n        <button class="nav-tab" onclick="switchTab(\'quality-report\')">بوابات الجودة وتقرير المراجع (ISA 700)</button>\n        <button class="nav-tab" onclick="switchTab(\'audit-trail\')">سجل التدقيق الرقمي</button>\n    </div>\n\n    <!-- 1. Dashboard -->\n    <div id="tab-dashboard" class="tab-content active">\n        <div class="kpi-grid">\n            <div class="kpi-card">\n                <span class="kpi-title">ارتباطات المراجعة النشطة</span>\n                <span class="kpi-value" id="kpi-engagements">1</span>\n                <span class="kpi-sub">شركة الرواد للتجارة والصناعة (2026)</span>\n            </div>\n            <div class="kpi-card">\n                <span class="kpi-title">نسبة إنجاز إجراءات المراجعة</span>\n                <span class="kpi-value" id="kpi-completion">100%</span>\n                <span class="kpi-sub">12 من 12 إجراء مكتمل وموثق</span>\n            </div>\n            <div class="kpi-card">\n                <span class="kpi-title">مخاطر التحريف الجوهري (ISA 315)</span>\n                <span class="kpi-value" id="kpi-risks">4</span>\n                <span class="kpi-sub">منها خطرين هامين (Significant)</span>\n            </div>\n            <div class="kpi-card">\n                <span class="kpi-title">الملاحظات والتحريفات المفتوحة</span>\n                <span class="kpi-value" id="kpi-notes">0</span>\n                <span class="kpi-sub">تم إغلاق وتسوية جميع الملاحظات</span>\n            </div>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">حالة دورة المراجعة الكاملة للارتباط الحالي</h2>\n                <span class="badge badge-success">جاهز للإصدار النهائي</span>\n            </div>\n            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; text-align: center;">\n                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border: 1px solid #bbf7d0;">\n                    <div style="font-weight: 700; color: #166534;">1. قبول العميل</div>\n                    <div style="font-size: 0.8rem; color: #15803d; margin-top: 0.25rem;">مكتمل ومجاز</div>\n                </div>\n                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border: 1px solid #bbf7d0;">\n                    <div style="font-weight: 700; color: #166534;">2. استيراد الميزان</div>\n                    <div style="font-size: 0.8rem; color: #15803d; margin-top: 0.25rem;">متوازن ومصنف آلياً</div>\n                </div>\n                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border: 1px solid #bbf7d0;">\n                    <div style="font-weight: 700; color: #166534;">3. الأهمية والمخاطر</div>\n                    <div style="font-size: 0.8rem; color: #15803d; margin-top: 0.25rem;">معتمدة (ISA 320/315)</div>\n                </div>\n                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border: 1px solid #bbf7d0;">\n                    <div style="font-weight: 700; color: #166534;">4. العمل الميداني</div>\n                    <div style="font-size: 0.8rem; color: #15803d; margin-top: 0.25rem;">أوراق العمل والأدلة</div>\n                </div>\n                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border: 1px solid #bbf7d0;">\n                    <div style="font-weight: 700; color: #166534;">5. مراجعة الجودة EQCR</div>\n                    <div style="font-size: 0.8rem; color: #15803d; margin-top: 0.25rem;">معتمد من الشريك المستقل</div>\n                </div>\n                <div style="background: #eff6ff; padding: 1rem; border-radius: 8px; border: 1px solid #bfdbfe;">\n                    <div style="font-weight: 700; color: #1e40af;">6. تقرير المراجع</div>\n                    <div style="font-size: 0.8rem; color: #2563eb; margin-top: 0.25rem;">رأي غير متحفظ (نظيف)</div>\n                </div>\n            </div>\n        </div>\n    </div>\n\n    <!-- 2. Client & Acceptance -->\n    <div id="tab-acceptance" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">ملف العميل وتقييم القبول والاستمرار (ISA 210 / ISQM 1)</h2>\n                <span class="badge badge-success">تم القبول بنجاح</span>\n            </div>\n            <table>\n                <tr><th>معرف العميل</th><td>CL-RUWAD-01</td><th>الاسم التجاري</th><td>شركة الرواد للتجارة والصناعة</td></tr>\n                <tr><th>الرقم الضريبي (ZATCA)</th><td>300123456700003</td><th>النشاط الاقتصادي</th><td>تجارة الجملة والتجزئة والتصنيع</td></tr>\n                <tr><th>فحص الاستقلالية والنزاهة</th><td><span class="badge badge-success">مجاز (لا يوجد تضارب مصالح)</span></td><th>مستوى مخاطر العميل</th><td><span class="badge badge-warning">متوسط (Medium)</span></td></tr>\n                <tr><th>الشريك المسؤول</th><td>أ. محمد القحطاني (SOCPA Certified)</td><th>مدير الارتباط</th><td>أ. سارة العتيبي</td></tr>\n            </table>\n        </div>\n    </div>\n\n    <!-- 3. Trial Balance & Mapping -->\n    <div id="tab-tb" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">ميزان المراجعة المستورد والتحليل الذكي للشذوذ</h2>\n                <span class="badge badge-success">إجمالي المدين = إجمالي الدائن (14,250,000 ر.س)</span>\n            </div>\n            <div style="background: #fffbeb; border: 1px solid #fef3c7; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;">\n                <strong>تنبيهات المحرك التحليلي للأنماط غير الطبيعية:</strong>\n                <ul style="margin-right: 1.5rem; font-size: 0.85rem; color: #92400e;">\n                    <li>تم كشف رصيد دائن غير اعتيادي بحساب الصندوق الفرعي بمبلغ (45,000 ر.س) - تم توجيه إجراء تدقيق مباشر وتعديله.</li>\n                    <li>تسجيل نمو في المبيعات بنسبة 28% مقارنة بالعام السابق - تم تصنيفه كخطر تحريف جوهري وفق ISA 240.</li>\n                </ul>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>رقم الحساب</th>\n                        <th>اسم الحساب</th>\n                        <th>مدين (ر.س)</th>\n                        <th>دائن (ر.س)</th>\n                        <th>التصنيف المالي (IFRS)</th>\n                        <th>بند القوائم المالية</th>\n                        <th>حالة التصنيف</th>\n                    </tr>\n                </thead>\n                <tbody id="tb-table-body">\n                    <tr><td>1010</td><td>النقد وما في حكمه بالبنوك</td><td>2,450,000.00</td><td>-</td><td>أصول متداولة</td><td>النقد وما في حكمه</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>1200</td><td>العملاء والذمم المدينة التجارية</td><td>4,120,000.00</td><td>-</td><td>أصول متداولة</td><td>الذمم المدينة التجارية</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>1300</td><td>المخزون السلعي (بضاعة تامة الصنع)</td><td>3,500,000.00</td><td>-</td><td>أصول متداولة</td><td>المخزون</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>1500</td><td>الممتلكات والآلات والمعدات (PPE)</td><td>4,180,000.00</td><td>-</td><td>أصول غير متداولة</td><td>الممتلكات والآلات والمعدات</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>2010</td><td>الموردون والذمم الدائنة التجارية</td><td>-</td><td>2,850,000.00</td><td>التزامات متداولة</td><td>الذمم الدائنة التجارية</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>3010</td><td>رأس مال الشركة</td><td>-</td><td>5,000,000.00</td><td>حقوق الملكية</td><td>رأس المال</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>4010</td><td>إيرادات المبيعات والخدمات</td><td>-</td><td>12,400,000.00</td><td>الإيرادات</td><td>الإيرادات من العقود مع العملاء</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                    <tr><td>5010</td><td>تكلفة المبيعات المباشرة</td><td>8,200,000.00</td><td>-</td><td>تكلفة المبيعات</td><td>تكلفة المبيعات</td><td><span class="badge badge-success">معتمد آلياً</span></td></tr>\n                </tbody>\n            </table>\n        </div>\n    </div>\n\n    <!-- 4. Materiality & Risks -->\n    <div id="tab-materiality-risk" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">الأهمية النسبية المعتمدة (ISA 320)</h2>\n                <span class="badge badge-info">المعيار الأساسي: الأرباح قبل الزكاة والضريبة</span>\n            </div>\n            <table>\n                <tr><th>الأهمية النسبية العامة (Overall Materiality - 5%)</th><td><strong>110,000.00 ر.س</strong></td><th>الأهمية النسبية للأداء (Performance Materiality - 75%)</th><td><strong>82,500.00 ر.س</strong></td></tr>\n                <tr><th>عتبة الخطأ التافه (Clearly Trivial Threshold - 5%)</th><td><strong>5,500.00 ر.س</strong></td><th>المبرر المهني للمراجع</th><td>تم اختيار 5% من الأرباح قبل الزكاة نظرًا لاستقرار النشاط التجاري وعدم وجود تعثر مالي.</td></tr>\n            </table>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">مصفوفة تقييم المخاطر (ISA 315 Revised)</h2>\n                <span class="badge badge-danger">4 مخاطر رئيسية محددة</span>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>بند الحساب</th>\n                        <th>وصف الخطر المحتمل</th>\n                        <th>الادعاء (Assertion)</th>\n                        <th>الخطر الكامن</th>\n                        <th>خطر الرقابة</th>\n                        <th>تقييم RMM</th>\n                        <th>الاستجابة الرقابية المخططة</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr><td>الإيرادات</td><td>خطر تضخيم المبيعات بنهاية السنة أو الاعتراف المبكر</td><td>الوجود والفصل الزمني</td><td>مرتفع</td><td>متوسط</td><td><span class="badge badge-danger">هام (Significant)</span></td><td>فحص فواتير المبيعات وبوالص الشحن واختبار Cut-off للمبيعات</td></tr>\n                    <tr><td>المخزون</td><td>خطر تقادم المخزون وعدم كفاية مخصص انخفاض القيمة</td><td>التقييم والتوزيع</td><td>متوسط</td><td>متوسط</td><td><span class="badge badge-warning">متوسط (Medium)</span></td><td>حضور الجرد الفعلي واختبار صافي القيمة القابلة للتحقق (NRV)</td></tr>\n                    <tr><td>النقد وما في حكمه</td><td>خطر وجود تسويات معلقة غير مسجلة أو تحويلات مكررة</td><td>الوجود والاكتمال</td><td>مرتفع</td><td>منخفض</td><td><span class="badge badge-info">متوسط (Medium)</span></td><td>مصادقات بنكية مباشرة لـ 100% من الحسابات ومطابقة التسويات</td></tr>\n                    <tr><td>الذمم المدينة</td><td>خطر تعثر ديون قديمة وعدم تكوين مخصص خسائر ائتمانية</td><td>التقييم والدقة</td><td>مرتفع</td><td>متوسط</td><td><span class="badge badge-danger">هام (Significant)</span></td><td>فحص نموذج IFRS 9 للأعمار الزمنية ومصادقة أرصدة كبار العملاء</td></tr>\n                </tbody>\n            </table>\n        </div>\n    </div>\n\n    <!-- 5. Working Papers -->\n    <div id="tab-working-papers" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">أوراق العمل الإلكترونية (ISA 230 Electronic Working Papers)</h2>\n                <span class="badge badge-success">جميع الأوراق أعدت وروجعت بالكامل</span>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>معرف ورقة العمل</th>\n                        <th>عنوان ورقة العمل</th>\n                        <th>الهدف من الإجراء</th>\n                        <th>الادعاء المغطى</th>\n                        <th>العينة المختارة</th>\n                        <th>النتيجة والاستنتاج</th>\n                        <th>المعد والمراجع</th>\n                        <th>الحالة</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr>\n                        <td>WP-REV-001</td>\n                        <td>اختبار تفاصيل المبيعات والفصل الزمني</td>\n                        <td>التأكد من صحة ووجود المبيعات المنفذة</td>\n                        <td>الوجود والقطع الزمني</td>\n                        <td>45 فاتورة مبيعات (MUS)</td>\n                        <td>المبيعات مسجلة في فترتها الصحيحة وتوجد مستندات استلام معتمدة.</td>\n                        <td>أعده: المدقق | راجعه: المدير</td>\n                        <td><span class="badge badge-success">معتمد ومغلق</span></td>\n                    </tr>\n                    <tr>\n                        <td>WP-BNK-001</td>\n                        <td>مطابقة الأرصدة البنكية ومذكرات التسوية</td>\n                        <td>التحقق من صحة واكتمال الأرصدة البنكية</td>\n                        <td>الوجود والحقوق</td>\n                        <td>100% من البنوك (3 بنوك)</td>\n                        <td>وردت مصادقات البنوك متطابقة ولا توجد فروقات جوهرية معلقة.</td>\n                        <td>أعده: المدقق | راجعه: المدير</td>\n                        <td><span class="badge badge-success">معتمد ومغلق</span></td>\n                    </tr>\n                    <tr>\n                        <td>WP-INV-001</td>\n                        <td>حضور الجرد الفعلي واختبار تقييم المخزون</td>\n                        <td>التحقق من الوجود الفعلي وحالة المخزون</td>\n                        <td>الوجود والتقييم</td>\n                        <td>عينة جرد 60 صنف</td>\n                        <td>تم حضور الجرد بمستودعات الرياض وجدة وتطابقت الكميات مع الدفاتر.</td>\n                        <td>أعده: المدقق | راجعه: الشريك</td>\n                        <td><span class="badge badge-success">معتمد ومغلق</span></td>\n                    </tr>\n                </tbody>\n            </table>\n        </div>\n    </div>\n\n    <!-- 6. Sampling & Confirmations -->\n    <div id="tab-sampling-confirmations" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">محرك العينات الإحصائية (ISA 530 Monetary Unit Sampling)</h2>\n                <span class="badge badge-info">MUS & Systematic Sampling</span>\n            </div>\n            <table>\n                <tr><th>المجتمع المفحوص (Population)</th><td>12,400,000.00 ر.س (مبيعات السنة)</td><th>الأهمية المقبولة (Tolerable Error)</th><td>82,500.00 ر.س</td></tr>\n                <tr><th>مستوى الثقة الإحصائي</th><td>95% (معامل التوسع 3.0)</td><th>فاصل المعاينة (Sampling Interval)</th><td>27,500.00 ر.س</td></tr>\n                <tr><th>حجم العينة المقترح والمختار</th><td><strong>45 بندًا رئيسيًا</strong></td><th>المنهجية</th><td>فحص 100% للبنود الأكبر من فاصل المعاينة + عينة منتظمة للباقي</td></tr>\n            </table>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">سجل المصادقات الخارجية (ISA 505 External Confirmations)</h2>\n                <span class="badge badge-success">اكتمال ورود المصادقات 100%</span>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>الجهة المستلمة</th>\n                        <th>نوع المصادقة</th>\n                        <th>الرصيد الدفتري</th>\n                        <th>الرصيد المصادق عليه</th>\n                        <th>الفارق</th>\n                        <th>تاريخ الرد</th>\n                        <th>حالة المصادقة</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr><td>مصرف الراجحي</td><td>بنك</td><td>1,850,000.00 ر.س</td><td>1,850,000.00 ر.س</td><td>0.00</td><td>2026-02-15</td><td><span class="badge badge-success">متطابقة ومغلقة</span></td></tr>\n                    <tr><td>البنك الأهلي السعودي</td><td>بنك</td><td>600,000.00 ر.س</td><td>600,000.00 ر.س</td><td>0.00</td><td>2026-02-16</td><td><span class="badge badge-success">متطابقة ومغلقة</span></td></tr>\n                    <tr><td>شركة التوريدات العالمية</td><td>مورد رئيسي</td><td>1,200,000.00 ر.س</td><td>1,200,000.00 ر.س</td><td>0.00</td><td>2026-02-20</td><td><span class="badge badge-success">متطابقة ومغلقة</span></td></tr>\n                    <tr><td>شركة منافذ التوزيع المتحدة</td><td>عميل رئيسي</td><td>950,000.00 ر.س</td><td>950,000.00 ر.س</td><td>0.00</td><td>2026-02-22</td><td><span class="badge badge-success">متطابقة ومغلقة</span></td></tr>\n                </tbody>\n            </table>\n        </div>\n    </div>\n\n    <!-- 7. Review Notes & Misstatements -->\n    <div id="tab-review-misstatements" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">ملاحظات المراجعة (Review Notes)</h2>\n                <span class="badge badge-success">0 ملاحظات معلقة</span>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>الملاحظة</th>\n                        <th>المثير</th>\n                        <th>المسؤول</th>\n                        <th>الرد والإجراء التصحيحي</th>\n                        <th>الحالة</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr>\n                        <td>معالجة الرصيد الدائن بحساب الصندوق الفرعي</td>\n                        <td>مدير الارتباط</td>\n                        <td>المدقق الميداني</td>\n                        <td>تم فحص السندات المعلقة وتبين وجود تسوية نقدية بمبلغ 45,000 ر.س تم قيدها بتاريخ لاحق، وتم إجراء قيد التسوية المطلوب.</td>\n                        <td><span class="badge badge-success">تم الاعتماد والإغلاق</span></td>\n                    </tr>\n                </tbody>\n            </table>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">سجل التحريفات والتسويات (ISA 450 Misstatements & Adjustments)</h2>\n                <span class="badge badge-success">التحريفات غير المعدلة أقل بكثير من الأهمية النسبية</span>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>الوصف</th>\n                        <th>المبلغ (ر.س)</th>\n                        <th>نوع التحريف</th>\n                        <th>هل تم تعديل الدفاتر؟</th>\n                        <th>الأثر على الأرباح</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr>\n                        <td>قيد تسوية سلف الموظفين والصندوق المعلق</td>\n                        <td>45,000.00</td>\n                        <td>فعلي (Factual)</td>\n                        <td><span class="badge badge-success">نعم (تم التعديل)</span></td>\n                        <td>0.00</td>\n                    </tr>\n                    <tr>\n                        <td>فارق طفيف في احتساب استهلاك أصل صغير</td>\n                        <td>3,200.00</td>\n                        <td>حكمي (Judgmental)</td>\n                        <td><span class="badge badge-warning">لا (أقل من الخطأ التافه 5,500)</span></td>\n                        <td>-3,200.00</td>\n                    </tr>\n                </tbody>\n            </table>\n            <div style="margin-top: 1rem; padding: 0.75rem; background: #f8fafc; border-radius: 8px; font-size: 0.85rem;">\n                <strong>التقييم النهائي للتحريفات:</strong> إجمالي الأخطاء غير المعدلة = 3,200 ر.س وهو أقل من عتبة الخطأ التافه (5,500 ر.س) وأقل بكثير من أهمية الأداء (82,500 ر.س)، وبالتالي لا تؤثر جوهريًا على عدالة القوائم المالية.\n            </div>\n        </div>\n    </div>\n\n    <!-- 8. Quality Gates & Report -->\n    <div id="tab-quality-report" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">بوابات الجودة ومراجعة الارتباط المستقلة (ISA 220 / ISQM 2 EQCR)</h2>\n                <span class="badge badge-success">تم اجتياز جميع البوابات بنجاح 100%</span>\n            </div>\n\n            <div class="gate-box gate-passed">\n                <div>\n                    <strong>البوابة 1: قبول العميل واستمراره (Client Acceptance)</strong>\n                    <div style="font-size: 0.8rem; color: #166534;">اجتياز متطلبات الاستقلالية والنزاهة وتعيين فريق مؤهل ومرخص.</div>\n                </div>\n                <span class="badge badge-success">مكتملة ومجازة</span>\n            </div>\n\n            <div class="gate-box gate-passed">\n                <div>\n                    <strong>البوابة 2: اكتمال التخطيط واعتماد الأهمية والمخاطر (Planning & Risk Gate)</strong>\n                    <div style="font-size: 0.8rem; color: #166534;">ميزان المراجعة متوازن، الحسابات مصنفة، مصفوفة ISA 315 مكتملة، والأهمية معتمدة.</div>\n                </div>\n                <span class="badge badge-success">مكتملة ومجازة</span>\n            </div>\n\n            <div class="gate-box gate-passed">\n                <div>\n                    <strong>البوابة 3: اكتمال إجراءات العمل الميداني والتوثيق (Fieldwork & ISA 230 Gate)</strong>\n                    <div style="font-size: 0.8rem; color: #166534;">جميع أوراق العمل مكتملة ومدعمة بالأدلة، المصادقات مكتملة، ولا توجد إجراءات معلقة.</div>\n                </div>\n                <span class="badge badge-success">مكتملة ومجازة</span>\n            </div>\n\n            <div class="gate-box gate-passed">\n                <div>\n                    <strong>البوابة 4: مراجعة الجودة النهائية وإذن إصدار التقرير (EQCR Sign-off)</strong>\n                    <div style="font-size: 0.8rem; color: #166534;">اعتماد مراجع الجودة المستقل، تسوية الملاحظات، وإقرار الرأي غير المتحفظ.</div>\n                </div>\n                <span class="badge badge-success">معتمد وموقع</span>\n            </div>\n        </div>\n\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">تقرير مراجع الحسابات المستقل (Independent Auditor\'s Report)</h2>\n                <button class="btn btn-primary" onclick="alert(\'تم تجهيز التقرير وفق متطلبات الهيئة السعودية للمراجعين والمحاسبين SOCPA ومعايير ISA.\')">طباعة / تصدير التقرير</button>\n            </div>\n            <pre>\n================================================================================\n                      تقرير مراجع الحسابات المستقل\n                     INDEPENDENT AUDITOR\'S REPORT\n================================================================================\nإلى السادة / مساهمي شركة شركة الرواد للتجارة والصناعة\nالرياض - المملكة العربية السعودية\n\nأولاً: الرأي غير المتحفظ (Unmodified Opinion):\nراجعنا القوائم المالية لشركة شركة الرواد للتجارة والصناعة ("الشركة")، والتي تشتمل على\nقائمة المركز المالي كما في 31 ديسمبر 2026م، وقائمة الربح أو الخسارة والدخل الشامل الآخر،\nوقائمة التغيرات في حقوق الملكية، وقائمة التدفقات النقدية للسنة المنتهية في ذلك التاريخ،\nوالإيضاحات المرفقة بالقوائم المالية بما في ذلك ملخص السياسات المحاسبية الهامة.\n\nوفي رأينا، فإن القوائم المالية المرفقة تظهر بعدالة، من كافة النواحي الجوهرية،\nالمركز المالي لشركة شركة الرواد للتجارة والصناعة كما في 31 ديسمبر 2026م، وأداءها المالي\nوتدفقاتها النقدية للسنة المنتهية في ذلك التاريخ وفقاً للمعايير الدولية للتقرير المالي (IFRS)\nالمعتمدة في المملكة العربية السعودية والمعايير والإصدارات الأخرى المعتمدة من الهيئة\nالسعودية للمراجعين والمحاسبين (SOCPA).\n\nثانياً: أساس الرأي (Basis for Opinion):\nتمت مراجعتنا وفقاً للمعايير الدولية للمراجعة المعتمدة في المملكة العربية السعودية (ISA).\nونحن مستقلون عن الشركة وفقاً لقواعد سلوك وآداب المهنة المعتمدة في المملكة، ونعتقد أن\nأدلة المراجعة التي حصلنا عليها كافية ومناسبة لتوفير أساس لرأينا.\n\nثالثاً: أمور المراجعة الرئيسية (Key Audit Matters - ISA 701):\n1. الاعتراف بالإيرادات والتحقق من الفصل الزمني (Revenue Recognition & Cut-off).\n2. تقييم المخزون وصافي القيمة القابلة للتحقق (Inventory Valuation & NRV).\n\nعن مكتب المراجعة: My Audit Chartered Accountants & Auditors\nالشريك المسؤول: أ. محمد القحطاني (SOCPA License No. 492)\nالرياض، المملكة العربية السعودية\n================================================================================\n            </pre>\n        </div>\n    </div>\n\n    <!-- 9. Audit Trail -->\n    <div id="tab-audit-trail" class="tab-content">\n        <div class="card">\n            <div class="card-header">\n                <h2 class="card-title">سجل التدقيق الرقمي غير القابل للتعديل (Immutable Audit Trail)</h2>\n                <span class="badge badge-info">متوافق مع نظام حماية البيانات الشخصية السعودي PDPL</span>\n            </div>\n            <table>\n                <thead>\n                    <tr>\n                        <th>المستخدم</th>\n                        <th>الإجراء</th>\n                        <th>الكائن المعني</th>\n                        <th>المعرف</th>\n                        <th>التفاصيل والملاحظات</th>\n                        <th>التوقيت والختم الزمني</th>\n                    </tr>\n                </thead>\n                <tbody>\n                    <tr><td>EQCR Partner</td><td>APPROVE</td><td>quality_reviews</td><td>EQC-001</td><td>اعتماد مراجعة جودة الارتباط والموافقة على إصدار الرأي النظيف</td><td>2026-09-09 18:45:00</td></tr>\n                    <tr><td>Engagement Partner</td><td>APPROVE</td><td>materiality</td><td>MAT-001</td><td>اعتماد الأهمية النسبية العامة 110,000 ر.س وأهمية الأداء 82,500 ر.س</td><td>2026-09-09 18:10:00</td></tr>\n                    <tr><td>Senior Auditor</td><td>CREATE</td><td>working_papers</td><td>WP-REV-001</td><td>توثيق اختبار تفاصيل المبيعات وعينة MUS المعتمدة بنجاح</td><td>2026-09-09 18:25:00</td></tr>\n                    <tr><td>Staff Auditor</td><td>IMPORT</td><td>trial_balances</td><td>TB-001</td><td>استيراد ميزان المراجعة وتأكيد توازن المدين والدائن 14,250,000 ر.س</td><td>2026-09-09 18:05:00</td></tr>\n                    <tr><td>Admin</td><td>CREATE</td><td>clients</td><td>CL-RUWAD-01</td><td>تسجيل ملف العميل الجديد وإجراء تقييم القبول والاستقلالية</td><td>2026-09-09 18:00:00</td></tr>\n                </tbody>\n            </table>\n        </div>\n    </div>\n\n</div>\n\n<script>\n    function switchTab(tabId) {\n        document.querySelectorAll(\'.nav-tab\').forEach(b => b.classList.remove(\'active\'));\n        document.querySelectorAll(\'.tab-content\').forEach(c => c.classList.remove(\'active\'));\n\n        event.target.classList.add(\'active\');\n        document.getElementById(\'tab-\' + tabId).classList.add(\'active\');\n    }\n</script>\n\n</body>\n</html>\n'

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
    conn.execute("PRAGMA foreign_keys = OFF;")

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
    populate_sample_audit()
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
