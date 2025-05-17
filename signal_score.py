import re

SCORING_RULES = {
    "words": {
        "alpha": 1,
        "drop": 1,
        "launch": 1,
        "airdrop": 1,
        "presale": 1
    },
    "emojis": {
        "🚀": 1.5,
        "🔥": 1.2,
        "💰": 1,
        "📈": 1
    },
    "phrases": {
        "airdrop incoming": 2,
        "token launch": 1.5,
        "new project": 1
    }
}

def score_message(content: str) -> float:
    content = content.lower()
    tokens = re.findall(r'\w+|[^\w\s]', content, re.UNICODE)

    score = 0
    total_possible = sum(SCORING_RULES["words"].values()) + \
                     sum(SCORING_RULES["emojis"].values()) + \
                     sum(SCORING_RULES["phrases"].values())

    for word in SCORING_RULES["words"]:
        if word in tokens:
            score += SCORING_RULES["words"][word]

    for emoji in SCORING_RULES["emojis"]:
        if emoji in content:
            score += SCORING_RULES["emojis"][emoji]

    for phrase in SCORING_RULES["phrases"]:
        if phrase in content:
            score += SCORING_RULES["phrases"][phrase]

    return round(score / total_possible, 4) if total_possible else 0