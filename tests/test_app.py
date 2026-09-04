from __future__ import annotations

import pytest
from textual.widgets import Input, Select, Static, Switch

from qwen38tui.app import Qwen38App
from qwen38tui.config import ServerConfig


@pytest.fixture
def app(inv, hw, monkeypatch, tmp_path):
    import qwen38tui.app as appmod
    import qwen38tui.config as cfgmod

    monkeypatch.setattr(appmod, "discover_all", lambda: inv)
    monkeypatch.setattr(appmod, "probe", lambda: hw)
    monkeypatch.setattr(appmod, "CURRENT_CONFIG", tmp_path / "current.json")
    monkeypatch.setattr(cfgmod, "PROFILES_DIR", tmp_path / "profiles")
    monkeypatch.setattr(appmod, "list_profiles", cfgmod.list_profiles)
    return Qwen38App()


async def test_app_renders_and_reacts(app):
    async with app.run_test(size=(160, 50)) as pilot:
        mem = app.query_one("#mem", Static)
        assert "Speicherbedarf" in str(mem.render())
        cmd = app.query_one("#cmd", Static)
        assert "serve" in str(cmd.render())
        # Kontext ändern -> Config folgt
        inp = app.query_one("#f-ctx_size", Input)
        inp.value = "65536"
        await pilot.pause()
        assert app.cfg.ctx_size == 65536
        # MTP aus -> kein -md im Kommando
        sw = app.query_one("#f-mtp_enabled", Switch)
        sw.value = False
        await pilot.pause()
        assert app.cfg.mtp_enabled is False
        assert "-md" not in str(app.query_one("#cmd", Static).render())
        # Quant wählen
        sel = app.query_one("#f-quant", Select)
        sel.value = "UD-Q2_K_XL"
        await pilot.pause()
        assert app.cfg.quant == "UD-Q2_K_XL"


async def test_preset_apply(app):
    async with app.run_test(size=(160, 50)) as pilot:
        app.query_one("#preset-select", Select).value = "stock-max-speed"
        await pilot.click("#btn-preset")
        await pilot.pause()
        assert app.cfg.quant == "UD-Q2_K_XL" and app.cfg.ctx_size == 32768
        assert app.query_one("#f-quant", Select).value == "UD-Q2_K_XL"


async def test_tabs_exist(app):
    async with app.run_test(size=(160, 50)) as pilot:
        from textual.widgets import TabbedContent

        tc = app.query_one(TabbedContent)
        for tab in ("tab-srv", "tab-bench", "tab-sys", "tab-help"):
            tc.active = tab
            await pilot.pause()
        assert app.query_one("#sys-table")
