import math
from typing import Dict, Any, List

class SamplingEngine:
    """
    ISA 530 Audit Sampling Engine:
    Supports Monetary Unit Sampling (MUS), Random, Systematic, and 100% threshold sampling.
    """

    # Expansion factors for MUS based on risk/confidence (default 95% confidence ~ factor 3.0)
    CONFIDENCE_FACTORS = {
        0.90: 2.31,
        0.95: 3.00,
        0.99: 4.61
    }

    @classmethod
    def calculate_mus_sample_size(
        cls,
        population_value: float,
        tolerable_misstatement: float,
        expected_misstatement: float = 0.0,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Monetary Unit Sampling (MUS / PPS) calculation.
        """
        factor = cls.CONFIDENCE_FACTORS.get(confidence_level, 3.00)
        net_tolerable = max(tolerable_misstatement - (expected_misstatement * 1.6), 1.0)
        sampling_interval = round(net_tolerable / factor, 2)

        if sampling_interval <= 0:
            sample_size = 100
        else:
            sample_size = int(math.ceil(population_value / sampling_interval))

        # Practical cap between 5 and 200 items for testing efficiency
        sample_size = max(5, min(sample_size, 250))

        return {
            "method": "Monetary Unit Sampling (MUS)",
            "population_value": population_value,
            "tolerable_misstatement": tolerable_misstatement,
            "expected_misstatement": expected_misstatement,
            "confidence_level": confidence_level,
            "sampling_interval": sampling_interval,
            "recommended_sample_size": sample_size,
            "justification": f"حُسب حجم العينة بأسلوب MUS مع فاصل معاينة {sampling_interval:,.2f} ر.س ومستوى ثقة {int(confidence_level*100)}% طبقًا للمعيار الدولي ISA 530."
        }

    @classmethod
    def select_systematic_samples(cls, items: List[Dict[str, Any]], sample_size: int) -> List[Dict[str, Any]]:
        """
        Selects items systematically based on interval.
        """
        if not items:
            return []
        n = len(items)
        if sample_size >= n:
            return items

        step = n / sample_size
        selected = []
        for i in range(sample_size):
            idx = int(i * step)
            selected.append(items[idx])
        return selected
