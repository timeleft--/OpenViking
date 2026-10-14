# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: AGPL-3.0

import pytest

from openviking.models.model_error import ModelError, ModelErrorKind
from openviking.storage.queuefs.retry_policy import is_queue_retryable


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        (ModelErrorKind.TRANSIENT_SERVICE_ERROR, True),
        (ModelErrorKind.TRANSIENT_NETWORK_ERROR, True),
        (ModelErrorKind.RATE_LIMIT_ERROR, True),
        (ModelErrorKind.AUTHENTICATION_ERROR, False),
        (ModelErrorKind.PERMISSION_DENIED, False),
        (ModelErrorKind.QUOTA_EXHAUSTED, False),
        (ModelErrorKind.MODEL_NOT_FOUND, False),
        (ModelErrorKind.UNSUPPORTED, False),
        (ModelErrorKind.INVALID_REQUEST, False),
        (ModelErrorKind.INPUT_TOO_LARGE, False),
        (ModelErrorKind.CONTENT_SAFETY, False),
        (ModelErrorKind.UNKNOWN, False),
    ],
)
def test_queue_retryable_model_error_kinds(kind, expected):
    assert is_queue_retryable(ModelError(kind, "model request failed")) is expected


def test_unrecognized_error_is_not_queue_retryable():
    assert is_queue_retryable(RuntimeError("500 Internal Server Error")) is False
