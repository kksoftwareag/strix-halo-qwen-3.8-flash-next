from __future__ import annotations

from qwen38tui.bench import aggregate_level, check_crosstalk, make_user_prompts


def test_user_prompts_unique_codes():
    ps = make_user_prompts(8, seed=1)
    codes = [c for c, _ in ps]
    assert len(set(codes)) == 8
    assert all(c in p for c, p in ps)
    assert make_user_prompts(8, seed=1) == ps          # reproduzierbar


def test_crosstalk_detection():
    codes = ["KW1A", "KW2B", "KW3C"]
    assert not check_crosstalk("KW1A", "KW1A: hier die Antwort", codes)
    assert check_crosstalk("KW1A", "KW2B: Antwort eines anderen Slots", codes)
    assert check_crosstalk("KW1A", "Antwort ohne Codewort", codes)
    assert check_crosstalk("KW1A", "KW1A ... und KW3C", codes)


def test_aggregate_level_percentiles():
    users = [{"predicted_n": 100, "predicted_per_second": 10.0, "ttft": t, "prompt_per_second": 50.0} for t in (0.5, 1.0, 2.0, 4.0)]
    agg = aggregate_level(users, wall=20.0)
    assert agg["agg_tps"] == 400 / 20.0 and agg["gen_tokens"] == 400
    assert agg["user_tg_mean"] == 10.0 and agg["user_tg_min"] == 10.0
    assert agg["ttft_p50"] in (1.0, 2.0) and agg["ttft_p95"] == 4.0
    assert agg["pp_mean"] == 50.0
    assert aggregate_level([], 5.0)["agg_tps"] == 0.0
