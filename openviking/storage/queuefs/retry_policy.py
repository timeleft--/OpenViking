# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: AGPL-3.0
"""Shared limits for durable queue retry policies."""

from openviking.models.model_error import ModelErrorKind, model_error_from_exception

MAX_FAILURE_REQUEUE_COUNT = 2

_QUEUE_RETRYABLE_MODEL_ERROR_KINDS = frozenset(
    {
        ModelErrorKind.TRANSIENT_SERVICE_ERROR,
        ModelErrorKind.TRANSIENT_NETWORK_ERROR,
        ModelErrorKind.RATE_LIMIT_ERROR,
    }
)


def is_queue_retryable(error: BaseException) -> bool:
    """Return whether a normalized model error may be retried by a durable queue."""
    model_error = model_error_from_exception(error)
    return model_error is not None and model_error.kind in _QUEUE_RETRYABLE_MODEL_ERROR_KINDS
