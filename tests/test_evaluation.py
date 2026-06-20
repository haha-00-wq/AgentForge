from app.evaluation.datasets import EvaluationCase, load_jsonl_dataset
from app.evaluation.evaluator import ExactMatchScorer, run_batch_evaluation


def test_batch_evaluation_loads_jsonl_and_scores_exact_match(tmp_path):
    dataset = tmp_path / "cases.jsonl"
    dataset.write_text(
        '{"case_id":"c1","input":{"text":"hello"},"expected":{"label":"ok"},"actual":{"label":"ok"}}\n'
        '{"case_id":"c2","input":{"text":"bye"},"expected":{"label":"ok"},"actual":{"label":"bad"}}\n',
        encoding="utf-8",
    )

    cases = load_jsonl_dataset(dataset)
    results = run_batch_evaluation(cases, ExactMatchScorer(field="label"))

    assert [case.case_id for case in cases] == ["c1", "c2"]
    assert [result.score for result in results] == [1.0, 0.0]


def test_evaluation_case_can_be_constructed_directly():
    case = EvaluationCase(case_id="direct", input={"q": "x"}, expected={"a": "y"})

    assert case.actual == {}

