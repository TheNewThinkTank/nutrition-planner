import pytest
import httpx
from unittest.mock import AsyncMock, patch

from streamlit_app import get_nutritionix, main

# Mocked headers and URL for Nutritionix API
HEADER = {
    "Content-Type": "application/json",
    "x-app-id": "mock_id",
    "x-app-key": "mock_key",
}
URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

# Sample data for testing
sample_response = {
    "foods": [{
        "nf_protein": 10.0,
        "nf_total_fat": 5.0,
        "nf_total_carbohydrate": 20.0
    }]
}


@pytest.mark.asyncio
async def test_get_nutritionix_success():
    sample_response = {
        "foods": [
            {"nf_protein": 10.0, "nf_total_fat": 5.0, "nf_total_carbohydrate": 20.0}
            ]
        }
    async with httpx.AsyncClient() as client:
        with patch.object(
            client,
            "post",
            AsyncMock(return_value=httpx.Response(200, json=sample_response))
            ):
            result = await get_nutritionix(client, "1 cup of rice")
            assert result == {"protein": 10.0, "fat": 5.0, "carbs": 20.0}


@pytest.mark.asyncio
async def test_get_nutritionix_failure():
    # Test error handling with an invalid response
    async with httpx.AsyncClient() as client:
        with patch.object(client, "post", AsyncMock(return_value=httpx.Response(400))):
            result = await get_nutritionix(client, "1 cup of rice")
            assert result is None


@pytest.mark.asyncio
async def test_main():
    ingredients = [("rice", 1, "cup"), ("chicken", 100, "g")]
    responses = [
        {"protein": 10.0, "fat": 5.0, "carbs": 20.0},
        {"protein": 30.0, "fat": 10.0, "carbs": 0.0}
    ]
    with patch("streamlit_app.get_nutritionix", side_effect=responses):
        result = await main(ingredients)
        assert result["protein"] == 40.0
        assert result["fat"] == 15.0
        assert result["carbs"] == 20.0
