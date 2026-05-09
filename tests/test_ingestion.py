from src.ingestion import create_session, rate_limit, make_request, pagination, save_json
from requests.adapters import HTTPAdapter
from unittest.mock import patch, MagicMock

def test_create_session():
    session = create_session()
    adapter = session.get_adapter("https://")
    assert isinstance(adapter, HTTPAdapter)

@patch("time.sleep")
@patch("time.time")
def test_rate_limit(mock_time, mock_sleep):
    mock_time.side_effect = [10, 10]
    result = rate_limit(last_request_time=5, interval=6)
    mock_sleep.assert_called_once_with(1) 
    assert result == 10

@patch("src.ingestion.rate_limit")
def test_make_requests(mock_rate_limit):
    mock_rate_limit.return_value = 123
    session = MagicMock()
    fake_response = MagicMock()
    session.get.return_value = fake_response
    url = "http://example.com"
    params = {"q" : "test"}

    response, last_request_time = make_request(session, url, 0, params)
    assert response == fake_response
    assert last_request_time == 123



