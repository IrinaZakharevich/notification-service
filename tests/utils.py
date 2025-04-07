from unittest.mock import AsyncMock, MagicMock


def mock_scalar_result(return_value):
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = return_value

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    execute_mock = AsyncMock(return_value=mock_result)
    return execute_mock


def mock_scalar_result_all(return_value_list):
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = return_value_list

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    return AsyncMock(return_value=mock_result)
