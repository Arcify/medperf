import pytest
from unittest.mock import call

from medperf.tests.utils import rand_l
from medperf.commands.result import BenchmarkExecution
from medperf.entities import Dataset, Benchmark, Cube

PATCH_EXECUTION = "medperf.commands.result.create.{}"


@pytest.fixture
def cube(mocker):
    def cube_gen():
        cube = mocker.create_autospec(spec=Cube)
        cube.uid = 1
        return cube

    return cube_gen


@pytest.fixture
def execution(mocker, comms, ui, cube):
    mock_dset = mocker.create_autospec(spec=Dataset)
    mock_bmark = mocker.create_autospec(spec=Benchmark)
    mocker.patch(PATCH_EXECUTION.format("init_storage"))
    mocker.patch(PATCH_EXECUTION.format("Dataset"), side_effect=mock_dset)
    mocker.patch(PATCH_EXECUTION.format("Benchmark"), side_effect=mock_bmark)
    exec = BenchmarkExecution(0, 0, 0, comms, ui)
    exec.dataset.uid = 1
    exec.dataset.data_uid = "data_uid"
    exec.dataset.preparation_cube_uid = "prep_cube"
    exec.benchmark.data_preparation = "prep_cube"
    exec.benchmark.models = [0]
    exec.evaluator = cube()
    exec.model_cube = cube()
    return exec


def test_validate_fails_if_preparation_cube_mismatch(mocker, execution):
    # Arrange
    execution.dataset.preparation_cube_uid = "dset_prep_cube"
    execution.benchmark.data_preparation = "bmark_prep_cube"
    spy = mocker.patch(
        PATCH_EXECUTION.format("pretty_error"),
        side_effect=lambda *args, **kwargs: exit(),
    )

    # Act
    with pytest.raises(SystemExit):
        execution.validate()

    # Assert
    spy.assert_called_once()


@pytest.mark.parametrize("model_uid", rand_l(5, 5000, 5))
def test_validate_fails_if_model_not_in_benchmark(mocker, execution, model_uid):
    # Arrange
    execution.model_uid = model_uid  # model not in benchmark
    spy = mocker.patch(
        PATCH_EXECUTION.format("pretty_error"),
        side_effect=lambda *args, **kwargs: exit(),
    )

    # Act
    with pytest.raises(SystemExit):
        execution.validate()

    # Assert
    spy.assert_called_once()


def test_validate_passes_under_right_conditions(mocker, execution):
    # Arrange
    spy = mocker.patch(PATCH_EXECUTION.format("pretty_error"))

    # Act
    execution.validate()

    # Assert
    spy.assert_not_called()


@pytest.mark.parametrize("evaluator_uid", rand_l(1, 5000, 5))
@pytest.mark.parametrize("model_uid", rand_l(1, 5000, 5))
def test_get_cubes_retrieves_expected_cubes(
    mocker, execution, evaluator_uid, model_uid
):
    # Arrange
    spy = mocker.patch(
        PATCH_EXECUTION.format("BenchmarkExecution._BenchmarkExecution__get_cube")
    )
    execution.benchmark.evaluator = evaluator_uid
    execution.model_uid = model_uid
    evaluator_call = call(evaluator_uid, "Evaluator")
    model_call = call(model_uid, "Model")
    calls = [evaluator_call, model_call]

    # Act
    execution.get_cubes()

    # Assert
    spy.assert_has_calls(calls)


@pytest.mark.parametrize("cube_uid", rand_l(1, 5000, 5))
@pytest.mark.parametrize("name", [str(x) for x in rand_l(1, 500, 1)])
def test__get_cube_retrieves_cube(mocker, execution, cube_uid, name):
    # Arrange
    comms = execution.comms
    spy = mocker.patch(PATCH_EXECUTION.format("Cube.get"))
    mocker.patch(PATCH_EXECUTION.format("check_cube_validity"))

    # Act
    execution._BenchmarkExecution__get_cube(cube_uid, name)

    # Assert
    spy.assert_called_once_with(cube_uid, comms)


def test__get_cube_checks_cube_validity(mocker, execution, cube):
    # Arrange
    ui = execution.ui
    mocker.patch(PATCH_EXECUTION.format("Cube.get"), return_value=cube)
    spy = mocker.patch(PATCH_EXECUTION.format("check_cube_validity"))

    # Act
    execution._BenchmarkExecution__get_cube(1, "test")

    # Assert
    spy.assert_called_once_with(cube, ui)


def test_run_cubes_executes_expected_cube_tasks(mocker, execution):
    # Arrange
    execution.dataset.data_path = "data_path"
    execution.model_cube.cube_path = "cube_path"
    model_spy = mocker.patch.object(execution.model_cube, "run")
    eval_spy = mocker.patch.object(execution.evaluator, "run")
    mocker.patch("os.path.join", return_value="")
    mocker.patch(
        PATCH_EXECUTION.format("results_path"), return_value="",
    )

    # Act
    execution.run_cubes()

    # Assert
    assert model_spy.call_count == 1
    assert model_spy.call_args_list[0][1]["task"] == "infer"
    assert eval_spy.call_count == 1
    assert eval_spy.call_args_list[0][1]["task"] == "evaluate"


def test_run_executes_expected_flow(mocker, comms, ui, execution):
    # Arrange
    val_spy = mocker.patch(PATCH_EXECUTION.format("BenchmarkExecution.validate"))
    get_spy = mocker.patch(PATCH_EXECUTION.format("BenchmarkExecution.get_cubes"))
    run_spy = mocker.patch(PATCH_EXECUTION.format("BenchmarkExecution.run_cubes"))
    mocker.patch(PATCH_EXECUTION.format("cleanup"))

    # Act
    BenchmarkExecution.run(1, 1, 1, comms, ui)

    # Assert
    val_spy.assert_called_once()
    get_spy.assert_called_once()
    run_spy.assert_called_once()
