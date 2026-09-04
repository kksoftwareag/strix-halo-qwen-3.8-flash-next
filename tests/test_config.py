from __future__ import annotations

import json

from qwen38tui.config import ServerConfig, build_command
from qwen38tui.memory import fits


def _argmap(argv: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("-") and i + 1 < len(argv) and not argv[i + 1].startswith("-"):
            out[a] = argv[i + 1]
            i += 2
        else:
            out[a] = ""
            i += 1
    return out


def test_default_command_uses_mtp_and_env(inv, hw):
    cfg = ServerConfig(quant="UD-Q4_K_XL")
    cmd = build_command(cfg, inv, hw)
    assert cmd.ok, cmd.errors
    m = _argmap(cmd.argv)
    assert cmd.argv[1] == "serve"
    assert m["-m"].endswith("q4-00001-of-00004.gguf")
    assert m["--spec-type"] == "draft-mtp"
    assert m["-md"].endswith("mtp-dz.gguf")          # auto -> kompatibler Head (output_hc-Namen), nicht unsloth (hc_head)
    assert m["--spec-draft-n-max"] == "3"
    assert m["--spec-draft-p-min"] == "0.75"
    assert m["-ctk"] == "q8_0" and "LLAMA_ATTN_ROT_DISABLE" not in cmd.env     # Rotation bleibt an (verifiziert)
    cmd_rot = build_command(ServerConfig(quant="UD-Q4_K_XL", attn_rot_disable="on"), inv, hw)
    assert cmd_rot.env["LLAMA_ATTN_ROT_DISABLE"] == "1" and any("Rotation" in w for w in cmd_rot.warnings)
    assert json.loads(m["--chat-template-kwargs"]) == {"reasoning_effort": "medium"}
    assert m["--host"] == "10.50.4.9"
    assert "--tensor-read-lazy" not in m          # auto = llama-Default, wird nicht emittiert (EngramHalo kennt das Flag nicht)
    assert "--no-host" not in m and "--load-mode" not in m      # Default: auto (schneller Upload, PLE resident)
    assert any("PLE" in w for w in cmd.warnings)


def test_thinking_off_and_f16_kv(inv, hw):
    cfg = ServerConfig(quant="UD-Q2_K_XL", thinking=False, cache_type_k="f16", cache_type_v="f16", mtp_enabled=False, host="127.0.0.1")
    cmd = build_command(cfg, inv, hw)
    m = _argmap(cmd.argv)
    assert json.loads(m["--chat-template-kwargs"]) == {"enable_thinking": False}
    assert "LLAMA_ATTN_ROT_DISABLE" not in cmd.env
    assert "-md" not in m and "--spec-type" not in m
    assert m["--host"] == "127.0.0.1"


def test_engine_without_mtp_drops_draft_with_warning(inv, hw):
    cfg = ServerConfig(quant="UD-Q2_K_XL", engine="vk-test")
    cmd = build_command(cfg, inv, hw)
    assert cmd.ok
    assert cmd.argv[0].endswith("llama") and cmd.argv[1] != "serve"   # llama-server-Stil
    assert "-md" not in cmd.argv
    assert any("MTP" in w for w in cmd.warnings)


def test_auto_quant_picks_largest_fitting(inv, hw):
    cfg = ServerConfig(quant="auto")
    cmd = build_command(cfg, inv, hw, fits=lambda m: fits(cfg, m, inv.mtp_heads[0], hw))
    assert cmd.resolved.model.quant == "UD-Q2_K_XL"       # Q4_K_XL (103.7 GiB resident) passt nicht
    # mit lazy PLE (mmap) passt auch Q4_K_XL
    cfg2 = ServerConfig(quant="auto", load_mode="mmap")
    cmd2 = build_command(cfg2, inv, hw, fits=lambda m: fits(cfg2, m, inv.mtp_heads[0], hw))
    assert cmd2.resolved.model.quant == "UD-Q4_K_XL"


def test_invalid_reasoning_effort_is_normalized_and_ubatch_clamped():
    cfg = ServerConfig.from_dict({"reasoning_effort": "max", "ubatch_size": 4096, "batch_size": 2048})
    assert cfg.reasoning_effort == "medium"
    assert cfg.ubatch_size == 2048


def test_roundtrip_json(tmp_path):
    cfg = ServerConfig(ctx_size=65536, spec_draft_p_min=0.5, extra_env={"FOO": "1"})
    p = tmp_path / "c.json"
    cfg.save(p)
    back = ServerConfig.load(p)
    assert back == cfg


def test_script_export_contains_env_and_exec(inv, hw):
    from qwen38tui.scriptgen import bash_script

    cfg = ServerConfig(quant="UD-Q4_K_XL")
    cmd = build_command(cfg, inv, hw)
    sh = bash_script(cfg, cmd)
    assert "export LLAMA_ATTN_ROT_DISABLE" not in sh
    assert 'exec "$BIN" "${ARGS[@]}" "$@"' in sh
    assert "--spec-type draft-mtp" in sh


def test_default_counts_ple_resident_and_q4kxl_mtp_too_big(inv, hw):
    from qwen38tui.memory import estimate

    cfg = ServerConfig(quant="UD-Q4_K_XL")
    cmd = build_command(cfg, inv, hw)
    est = estimate(cfg, cmd.resolved.model, cmd.resolved.mtp, hw, "hip")
    assert est.ple_lazy == 0 and est.weights_resident == cmd.resolved.model.total_bytes
    assert est.verdict == "zu groß"


def test_mmap_enables_lazy_but_warns(inv, hw):
    from qwen38tui.memory import estimate

    cfg = ServerConfig(quant="UD-Q4_K_XL", load_mode="mmap")
    cmd = build_command(cfg, inv, hw)
    assert "--load-mode" in cmd.argv and "mmap" in cmd.argv
    assert any("18 MB/s" in w for w in cmd.warnings)
    est = estimate(cfg, cmd.resolved.model, cmd.resolved.mtp, hw, "hip")
    assert est.ple_lazy > 0


def test_incompatible_mtp_head_is_error(inv, hw):
    cfg = ServerConfig(quant="UD-Q2_K_XL", mtp_head="unsloth:mtp")
    cmd = build_command(cfg, inv, hw)
    assert not cmd.ok and any("hc_head" in e for e in cmd.errors)


def test_engramhalo_keeps_ple_lazy_and_q4kxl_fits(inv, hw):
    from qwen38tui.memory import estimate

    cfg = ServerConfig(quant="UD-Q4_K_XL", engine="eh-test", load_mode="none", tensor_read_lazy="on")
    cmd = build_command(cfg, inv, hw)
    assert cmd.ok, cmd.errors
    assert "--lazy-mode" in cmd.argv and "--tensor-read-lazy" not in cmd.argv
    assert "-lm" not in cmd.argv and "--load-mode" in cmd.argv and "none" in cmd.argv
    r = cmd.resolved
    est = estimate(cfg, r.model, r.mtp, hw, "hip", fast_lazy_ple=True)
    assert est.ple_lazy > 0 and est.verdict == "ok", est.rows()
