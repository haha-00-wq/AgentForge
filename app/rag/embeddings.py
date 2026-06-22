from __future__ import annotations

import math
import re
from collections import Counter


class SimpleEmbeddingModel:
    """本地简易 embedding 模型。

    功能:
        使用正则分词和词频归一化生成稀疏向量，适合测试和本地示例。
        生产环境可替换为 OpenAI、BGE、Ollama 等真实 embedding。
    """

    def embed(self, text: str) -> dict[str, float]:
        """将文本转换为稀疏向量。

        入参:
            text: 待向量化文本。

        出参:
            dict[str, float]: token 到归一化权重的映射。
        """
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        counts = Counter(tokens)
        norm = math.sqrt(sum(value * value for value in counts.values())) or 1.0
        return {token: value / norm for token, value in counts.items()}


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    """计算两个稀疏向量的余弦相似度。

    入参:
        left: 左侧稀疏向量。
        right: 右侧稀疏向量。

    出参:
        float: 相似度分数，越大表示越相关。
    """
    common = set(left) & set(right)
    return sum(left[token] * right[token] for token in common)
