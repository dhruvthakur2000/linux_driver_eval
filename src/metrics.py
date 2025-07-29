from src.logger import logger

def score_all(evaluation_data: dict) -> dict:
    """
    Calculate weighted scores for all evaluation metrics.
    Weights:
      - Correctness (compilation + functionality): 40%
      - Security: 25%
      - Code Quality: 20%
      - Advanced Features (and performance): 15%
    """
    try:
        # Correctness
        compilation = evaluation_data.get("compilation", {})
        functionality = evaluation_data.get("functionality", {})

        correctness = 0.0
        if compilation.get("success"):
            correctness += 0.5  # compilation counts half
        correctness += functionality.get("score", 0.0) * 0.5  # functionality counts half

        # Security
        security = evaluation_data.get("security", {})
        security_score = security.get("score", 0.0)

        # Code Quality
        quality = evaluation_data.get("code_quality", {})
        quality_score = quality.get("score", 0.0)

        # Advanced Features
        advanced = evaluation_data.get("advanced_features", {})
        advanced_score = advanced.get("score", 0.0)

        # Weighted score
        overall_score = (
            correctness * 40
            + security_score * 25
            + quality_score * 20
            + advanced_score * 15
        )

        return {
            "scores": {
                "correctness": round(correctness * 100, 2),
                "security": round(security_score * 100, 2),
                "code_quality": round(quality_score * 100, 2),
                "advanced": round(advanced_score * 100, 2),
                "overall_score": round(overall_score, 2)
            }
        }

    except Exception as e:
        logger.error(f"Error calculating scores: {e}")
        return {"scores": {}}
