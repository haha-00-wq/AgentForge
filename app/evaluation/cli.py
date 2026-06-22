from __future__ import annotations

import argparse
import json

from app.evaluation.datasets import load_jsonl_dataset
from app.evaluation.evaluator import ExactMatchScorer, run_batch_evaluation


def main() -> None:
    """批量评估命令行入口。

    入参:
        通过命令行读取:
            dataset: JSONL 数据集路径。
            --field: ExactMatchScorer 要比较的字段，默认 label。

    出参:
        None。将 EvaluationResult 列表以 JSON 打印到标准输出。
    """
    parser = argparse.ArgumentParser(description="Run AgentForge batch evaluation.")
    parser.add_argument("dataset", help="Path to a JSONL evaluation dataset.")
    parser.add_argument("--field", default="label", help="Field name to compare in expected and actual.")
    args = parser.parse_args()

    cases = load_jsonl_dataset(args.dataset)
    results = run_batch_evaluation(cases, ExactMatchScorer(field=args.field))
    print(json.dumps([result.model_dump() for result in results], ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
