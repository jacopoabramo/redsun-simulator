from __future__ import annotations

from redsun_simulator.engine.bluesky._core import SingleAxisStage

def test_single_axis_stage() -> None:
    stage = SingleAxisStage(axis="x", step_size=100)
    assert stage.axis == "x"
    assert stage.step_size == 100
    assert stage.position == 0

    stage.position = 100
    assert stage.position == 100

    stage.position = 100.5
    assert stage.position == 100

    stage.position = -100.5
    assert stage.position == -100

    stage.home()
    assert stage.position == 0
