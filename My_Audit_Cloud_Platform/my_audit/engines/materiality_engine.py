from typing import Dict, Any

class MaterialityEngine:
    """
    ISA 320 Materiality Engine:
    Calculates Overall Materiality, Performance Materiality, and Clearly Trivial Threshold.
    """

    BENCHMARK_RANGES = {
        "ProfitBeforeTax": {"min_pct": 3.0, "max_pct": 10.0, "default_pct": 5.0, "arabic_name": "الأرباح قبل الضريبة والزكاة"},
        "Revenue": {"min_pct": 0.5, "max_pct": 2.0, "default_pct": 1.0, "arabic_name": "إجمالي الإيرادات"},
        "TotalAssets": {"min_pct": 0.5, "max_pct": 2.0, "default_pct": 1.0, "arabic_name": "إجمالي الأصول"},
        "Equity": {"min_pct": 1.0, "max_pct": 5.0, "default_pct": 2.0, "arabic_name": "حقوق الملكية"}
    }

    @classmethod
    def calculate(
        cls,
        benchmark_type: str,
        benchmark_amount: float,
        overall_percentage: float = None,
        performance_percentage: float = 75.0,
        trivial_percentage: float = 5.0,
        risk_level: str = "Medium"
    ) -> Dict[str, Any]:
        """
        Calculates materiality components based on ISA 320 guidelines.
        """
        if benchmark_type not in cls.BENCHMARK_RANGES:
            raise ValueError(f"Unknown benchmark: {benchmark_type}. Allowed: {list(cls.BENCHMARK_RANGES.keys())}")

        default_om_pct = cls.BENCHMARK_RANGES[benchmark_type]["default_pct"]
        om_pct = overall_percentage if overall_percentage is not None else default_om_pct

        overall_materiality = round(abs(benchmark_amount) * (om_pct / 100.0), 2)

        # Performance materiality: typically 50% for higher risk, 75% for lower risk
        if performance_percentage is None:
            if risk_level == "High":
                performance_percentage = 50.0
            elif risk_level == "Low":
                performance_percentage = 75.0
            else:
                performance_percentage = 65.0

        performance_materiality = round(overall_materiality * (performance_percentage / 100.0), 2)

        # Clearly Trivial Threshold (CTT): 3% to 5% of Overall Materiality
        trivial_pct = trivial_percentage if trivial_percentage is not None else 5.0
        trivial_threshold = round(overall_materiality * (trivial_pct / 100.0), 2)

        justification = (
            f"تم اختيار معيار '{cls.BENCHMARK_RANGES[benchmark_type]['arabic_name']}' بمبلغ {benchmark_amount:,.2f} ر.س "
            f"وتطبيق نسبة {om_pct}% للأهمية العامة، ونسبة {performance_percentage}% للأهمية التنفيذية بناءً على مستوى مخاطر "
            f"الارتباط ({risk_level})، وعتبة الخطأ التافه بنسبة {trivial_pct}% وفقًا لمتطلبات معيار المراجعة الدولي ISA 320."
        )

        return {
            "benchmark_type": benchmark_type,
            "benchmark_name_ar": cls.BENCHMARK_RANGES[benchmark_type]['arabic_name'],
            "benchmark_amount": benchmark_amount,
            "overall_percentage": om_pct,
            "overall_materiality": overall_materiality,
            "performance_percentage": performance_percentage,
            "performance_materiality": performance_materiality,
            "trivial_percentage": trivial_pct,
            "trivial_threshold": trivial_threshold,
            "justification": justification
        }
