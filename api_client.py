import logging
from collections.abc import Mapping
from typing import Any
from uuid import uuid4

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.exceptions import APIConnectionError

logger = logging.getLogger(__name__)

def _safe_payload(payload: Any) -> Any:
    sensitive_keys = {"authorization", "api_key", "apikey", "password", "secret", "token", "access_token", "refresh_token"}
    if isinstance(payload, Mapping):
        return {k: "***" if any(x in k.lower() for x in sensitive_keys) else _safe_payload(v) for k, v in payload.items()}
    if isinstance(payload, list):
        return [_safe_payload(v) for v in payload]
    return payload

class APIClient:
    def __init__(self, base_url: str, *, verify: bool = True, timeout: float = 30.0,
                 retries: int = 2, token: str | None = None,
                 headers: Mapping[str, str] | None = None):
        self.base_url = base_url.rstrip("/")
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        if headers:
            self.session.headers.update(headers)
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

        retry_policy = Retry(
            total=retries, connect=retries, read=retries, status=retries,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_policy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method: str, endpoint: str, *, params=None, json=None,
                headers=None, timeout=None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_id = str(uuid4())
        request_headers = dict(headers or {})
        request_headers.setdefault("X-Request-ID", request_id)
        logger.info("%s %s params=%s payload=%s", method.upper(), url, params, _safe_payload(json))
        try:
            response = self.session.request(method, url, params=params, json=json,
                                             headers=request_headers, timeout=timeout or self.timeout)
        except requests.RequestException as exc:
            raise APIConnectionError(f"Request failed: {method.upper()} {url}") from exc
        logger.info("%s %s", response.status_code, url)
        return response

    def get(self, endpoint, params=None, **kwargs):
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self.request("POST", endpoint, json=json if json is not None else data, **kwargs)

    def put(self, endpoint, data=None, json=None, **kwargs):
        return self.request("PUT", endpoint, json=json if json is not None else data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
