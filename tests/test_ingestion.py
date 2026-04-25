from src.ingestion import create_session, rate_limit, make_request, pagination, create_df
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

@patch("src.ingestion.make_request")
def test_pagination(mock_make_request):

    session = MagicMock()
    #resp_1
    resp_1 = MagicMock()
    resp_1.status_code = 200
    resp_1.json.return_value = {"results": [{"name": "file1_name.csv"}]}
    
    #reponse 2
    resp_2 = MagicMock()
    resp_2.status_code = 200
    resp_2.json.return_value = {"results": []}

    mock_make_request.side_effect = [
        (resp_1, 1), 
        (resp_2, 2)
    ]

    files = pagination(session)
    assert files == [{"name":"file1_name.csv"}]

@patch("src.ingestion.pagination")
def test_create_df_columns(mock_pagination):
    mock_pagination.return_value = [
        {"name": "file1.csv"},
        {"name": "file2.csv"},
    ]

    session = MagicMock()
    df = create_df(session)
    assert list(df.columns) == ["name"]
    assert len(df) == 2

@patch("src.ingestion.pagination")
def test_create_df_values(mock_pagination):
    mock_pagination.return_value = [
        {"name": "file1.csv"},
        {"name": "file2.csv"},
    ]

    session = MagicMock()
    df = create_df(session)
    assert df["name"].tolist() == ["file1.csv", "file2.csv"]
    
