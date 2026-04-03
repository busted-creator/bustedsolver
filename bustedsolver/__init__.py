"""
BustedSolver -- reCAPTCHA v3 Solver SDK
"""

import httpx

API_URL = "https://api.bustedcap.com"


class BustedSolver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = API_URL

    def solve(self, site_key, page_url, action="submit", proxy=None, proxy_type="HTTP", timeout=60):
        """
        Solve reCAPTCHA v3 and return the token string (sync).

        Args:
            site_key: reCAPTCHA site key (starts with 6L...)
            page_url: Full URL of the page with reCAPTCHA
            action: reCAPTCHA action string (default: "submit")
            proxy: Optional proxy (e.g. "user:pass@host:port")
            proxy_type: Proxy protocol -- "HTTP" or "SOCKS5" (default: "HTTP")
            timeout: Request timeout in seconds (default: 60)

        Returns:
            str: reCAPTCHA token

        Raises:
            BustedError: If solve fails or API returns error
        """
        payload = {"site_key": site_key, "page_url": page_url, "action": action}
        if proxy:
            payload["proxy"] = proxy
            payload["proxy_type"] = proxy_type

        try:
            r = httpx.post(
                f"{self.api_url}/api/solve",
                json=payload,
                headers={"X-API-Key": self.api_key},
                timeout=timeout,
            )
        except httpx.TimeoutException:
            raise BustedError("Request timed out")
        except Exception as e:
            raise BustedError(f"Connection error: {e}")

        return self._parse_solve(r)

    async def solve_async(self, site_key, page_url, action="submit", proxy=None, proxy_type="HTTP", timeout=60):
        """
        Solve reCAPTCHA v3 and return the token string (async).

        Args:
            site_key: reCAPTCHA site key (starts with 6L...)
            page_url: Full URL of the page with reCAPTCHA
            action: reCAPTCHA action string (default: "submit")
            proxy: Optional proxy (e.g. "user:pass@host:port")
            proxy_type: Proxy protocol -- "HTTP" or "SOCKS5" (default: "HTTP")
            timeout: Request timeout in seconds (default: 60)

        Returns:
            str: reCAPTCHA token

        Raises:
            BustedError: If solve fails or API returns error
        """
        payload = {"site_key": site_key, "page_url": page_url, "action": action}
        if proxy:
            payload["proxy"] = proxy
            payload["proxy_type"] = proxy_type

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.post(
                    f"{self.api_url}/api/solve",
                    json=payload,
                    headers={"X-API-Key": self.api_key},
                )
        except httpx.TimeoutException:
            raise BustedError("Request timed out")
        except Exception as e:
            raise BustedError(f"Connection error: {e}")

        return self._parse_solve(r)

    def _parse_solve(self, r):
        data = r.json()
        if r.status_code == 200 and data.get("status") == "success":
            return data["token"]

        detail = data.get("detail") or data.get("message") or str(data)
        if r.status_code == 401:
            raise BustedError(f"Auth failed: {detail}")
        elif r.status_code == 429:
            raise BustedError(f"Rate limited: {detail}")
        else:
            raise BustedError(f"Solve failed: {detail}")

    def usage(self):
        """
        Check API key usage and remaining requests (sync).

        Returns:
            dict with requests_used, requests_limit, rate_per_minute, expires_at
        """
        try:
            r = httpx.get(
                f"{self.api_url}/api/usage",
                headers={"X-API-Key": self.api_key},
                timeout=10,
            )
            return r.json()
        except Exception as e:
            raise BustedError(f"Usage check failed: {e}")

    async def usage_async(self):
        """
        Check API key usage and remaining requests (async).

        Returns:
            dict with requests_used, requests_limit, rate_per_minute, expires_at
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    f"{self.api_url}/api/usage",
                    headers={"X-API-Key": self.api_key},
                )
                return r.json()
        except Exception as e:
            raise BustedError(f"Usage check failed: {e}")


class BustedError(Exception):
    pass
