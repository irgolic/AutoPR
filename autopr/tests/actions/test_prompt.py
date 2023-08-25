import os
from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from autopr.actions.prompt import Inputs, PromptString
from autopr.actions.utils.prompt_context import PromptContext, PromptContextEntry
from autopr.models.executable import ExecutableId
from autopr.tests.mock_openai import mock_openai
from autopr.tests.utils import run_action_manually, create_ephemeral_main_service, run_action_manually_with_main


@pytest.mark.asyncio
async def test_caching(mocker):
    my_mock = MagicMock(side_effect=mock_openai)
    mocker.patch(
        "openai.ChatCompletion.acreate",
        new=my_mock,
    )

    inputs = {
        "prompt": "What should I make a fruit salad with?",
        "instructions": "I am trying to make a fruit salad, but I don't know what to put in it.",
    }

    main = create_ephemeral_main_service()

    await run_action_manually_with_main(
        main=main,
        action=ExecutableId("prompt"),
        inputs=inputs
    )

    assert my_mock.call_count == 1

    assert os.path.exists(
        os.path.join(
            ".autopr",
            "cache",
        )
    )

    # Shelve makes inconsistent names across platforms for the cache files, so we can't assert this
    # assert os.path.exists(
    #     os.path.join(
    #         ".autopr",
    #         "cache",
    #         "prompt.db",
    #     )
    # )

    await run_action_manually_with_main(
        main=main,
        action=ExecutableId("prompt"),
        inputs=inputs
    )

    assert my_mock.call_count == 1


def test_trim_context():
    inputs = Inputs(
        strategy="middle out",
        max_prompt_tokens=60,
    )
    context = PromptContext(
        __root__=[
            PromptContextEntry(
                heading="What I have in my kitchen",
                value="Apple, bananas, oranges, tomatoes, " * 50,
            ),
        ],
    )
    trimmed_context = PromptString.trim_context(context, inputs)
    assert trimmed_context.__root__[0].value == """Apple, bananas, oranges, tomatoes, Apple, bananas, oranges, tomatoes, Apple, banana


... (trimmed) ...


s, tomatoes, Apple, bananas, oranges, tomatoes, Apple, bananas, oranges, tomatoes, """

    inputs = Inputs(
        strategy="middle out",
        max_prompt_tokens=100,
    )
    context = PromptContext(
        __root__=[
            PromptContextEntry(
                heading="What I have in my kitchen",
                value="Apple, bananas, oranges, tomatoes, " * 50,
            ),
            PromptContextEntry(
                heading="What I have in my pantry",
                value="Flour, sugar, salt, pepper, " * 50,
            ),
            PromptContextEntry(
                heading="What I have in my fridge",
                value="Milk, eggs, cheese, " * 50,
            ),
        ],
    )
    trimmed_context = PromptString.trim_context(context, inputs)
    assert len(trimmed_context.__root__) == 3
    assert trimmed_context.__root__[0].value == """Apple, bananas, oranges, to


... (trimmed) ...


bananas, oranges, tomatoes, """
    assert trimmed_context.__root__[1].value == """Flour, sugar, sal


... (trimmed) ...


ar, salt, pepper, """
    assert trimmed_context.__root__[2].value == """Milk, eggs, cheese, Milk,


... (trimmed) ...


eese, Milk, eggs, cheese, """

    inputs = Inputs(
        strategy="middle out",
        max_prompt_tokens=100,
    )
    context = PromptContext(
        __root__=[
            PromptContextEntry(
                heading="What I have in my kitchen",
                value="Apple, bananas, oranges, tomatoes, " * 50,
            ),
            PromptContextEntry(
                heading="What I have in my pantry",
                value="Flour, sugar, salt, pepper, " * 50,
            ),
            PromptContextEntry(
                heading="What I have in my fridge",
                value="Milk, eggs, cheese, " * 50,
                priority=2,
            ),
        ],
    )
    trimmed_context = PromptString.trim_context(context, inputs)
    assert len(trimmed_context.__root__) == 1
    assert trimmed_context.__root__[0].heading == "What I have in my fridge"
    assert trimmed_context.__root__[0].value == """Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, chee


... (trimmed) ...


k, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, Milk, eggs, cheese, """
