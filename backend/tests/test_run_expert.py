import os
import pandas as pd
from unittest.mock import patch, MagicMock
from backend.app.run_expert.consultant import setup

@patch('backend.app.run_expert.consultant.os.getenv', return_value='test_key')
@patch('backend.app.run_expert.consultant.Consultant')
def test_setup_loads_data(MockConsultant, mock_getenv):
    consultant, data = setup()
    MockConsultant.assert_called_once_with(
        api_key='test_key',
        provider='openai',
        model='gpt-4o-mini',
        name='Consultant',
        word_limit=100,
    )
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
