import asyncio
import requests
import pydantic

from autopr.actions.base import Action


# The action's inputs
class Inputs(pydantic.BaseModel):
    endpoint_url: str
    headers: dict[str, str] = {}


# The action's outputs
class Outputs(pydantic.BaseModel):
    contents: str


class GetApiCallActions(Action[Inputs, Outputs]):
    """
    Call API endpoint URL and return the response
    """

    id = "make_api_call"

    async def run(self, inputs: Inputs) -> Outputs:
        response = requests.get(inputs.endpoint_url, headers=inputs.headers)
        if response.status_code == 200:
            return Outputs(contents=response.content.decode())
        else:
            raise Exception(f"API call failed with status code {response.status_code}")


# When you run this file
if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    asyncio.run(
        # Run the action manually
        run_action_manually(
            action=GetApiCallActions,
            inputs=Inputs(
                endpoint_url="https://jsonplaceholder.typicode.com/todos",
                headers={"Content-type": "application/json; charset=UTF-8"},
            ),
        )
    )
