import unittest
import pytest
from unittest.mock import patch
from interface.web import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('interface.web.load_data')
def test_index_get(mock_load_data, client):
    mock_load_data.return_value = ([], [], [])
    response = client.get('/')
    assert response.status_code == 200
    assert b"patients" in response.data

@patch('interface.web.load_data')
@patch('interface.web.assign_nurses_to_patients')
@patch('interface.web.save_schedule')
def test_index_post(mock_save_schedule, mock_assign_nurses, mock_load_data, client):
    mock_load_data.return_value = ([{'id': 1, 'name': 'Nurse A'}], [{'id': 1, 'complexity': 1}], [])
    mock_assign_nurses.return_value = [{'nurse': 'Nurse A', 'patient': 'Patient 1'}]

    response = client.post('/', data={
        'max_row_diff': '2',
        'complexity_1': '3'
    })
    assert response.status_code == 200
    #assert b"success" in response.data
    mock_save_schedule.assert_called_once()
    mock_assign_nurses.assert_called_once()

def test_index_post_invalid_data(client):
    response = client.post('/', data={'max_row_diff': '0'})
    assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
