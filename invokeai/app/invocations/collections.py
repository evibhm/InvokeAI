# Copyright (c) 2023 Kyle Schouviller (https://github.com/kyle0654)

from typing import Literal, Optional

import numpy as np
from pydantic import Field

from invokeai.app.util.misc import SEED_MAX, get_random_seed

from .baseinvocation import (
    BaseInvocation,
    InvocationContext,
    BaseInvocationOutput,
)


class IntCollectionOutput(BaseInvocationOutput):
    """A collection of integers"""

    type: Literal["int_collection"] = "int_collection"

    # Outputs
    collection: list[int] = Field(default=[], description="The int collection")


class RangeInvocation(BaseInvocation):
    """Creates a range"""

    type: Literal["range"] = "range"

    # Inputs
    start: int = Field(default=0, description="The start of the range")
    stop: int = Field(default=10, description="The stop of the range")
    step: int = Field(default=1, description="The step of the range")

    def invoke(self, context: InvocationContext) -> IntCollectionOutput:
        return IntCollectionOutput(
            collection=list(range(self.start, self.stop, self.step))
        )


class RandomRangeInvocation(BaseInvocation):
    """Creates a collection of random numbers"""

    type: Literal["random_range"] = "random_range"

    # Inputs
    low: int = Field(default=0, description="The inclusive low value")
    high: int = Field(
        default=np.iinfo(np.int32).max, description="The exclusive high value"
    )
    size: int = Field(default=1, description="The number of values to generate")
    seed: int = Field(
        ge=0,
        le=SEED_MAX,
        description="The seed for the RNG (omit for random)",
        default_factory=get_random_seed,
    )

    def invoke(self, context: InvocationContext) -> IntCollectionOutput:
        rng = np.random.default_rng(self.seed)
        return IntCollectionOutput(
            collection=list(rng.integers(low=self.low, high=self.high, size=self.size))
        )
