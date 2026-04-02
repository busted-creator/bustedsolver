# BustedSolver

Fast reCAPTCHA v3 solver API.

> Currently in early access. More features coming soon.

## Install

```
pip install git+https://github.com/busted-creator/bustedsolver.git
```

## Usage (Sync)

```python
from bustedsolver import BustedSolver

solver = BustedSolver("sk_live_your_key_here")

token = solver.solve(
    site_key="6Le...",           # reCAPTCHA site key from target page
    page_url="https://...",      # URL of page with reCAPTCHA
    action="submit",             # action string (default: "submit")
)

payload = {
    "g-recaptcha-response": token,
}
```

## Usage (Async)

```python
import asyncio
from bustedsolver import BustedSolver

solver = BustedSolver("sk_live_your_key_here")

async def main():
    token = await solver.solve_async(
        site_key="6Le...",
        page_url="https://...",
        action="submit",
    )

    # solve multiple tokens in parallel
    token1, token2 = await asyncio.gather(
        solver.solve_async("6Le...", "https://...", action="submit"),
        solver.solve_async("6Le...", "https://...", action="submit"),
    )

asyncio.run(main())
```

## Proxy Support

You can optionally pass a proxy for the solver to use:

```python
token = solver.solve(
    site_key="6Le...",
    page_url="https://target.com",
    action="submit",
    proxy="user:pass@host:port",
    proxy_type="HTTP",            # "HTTP" (default) or "SOCKS5"
)

# async version
token = await solver.solve_async(
    site_key="6Le...",
    page_url="https://target.com",
    action="submit",
    proxy="user:pass@host:port",
)
```

If no proxy is provided, the solver uses its own infrastructure.

## Find reCAPTCHA Info

Open target page source and search for:
- **site_key**: Search `render=` or `sitekey` (starts with `6L`)
- **action**: Search `grecaptcha.execute` (inside `{action: 'xxx'}`)
- **page_url**: The page URL

## Check Usage

```python
# sync
usage = solver.usage()
print(f"Used: {usage['requests_used']}/{usage['requests_limit']}")

# async
usage = await solver.usage_async()
```

## Error Handling

```python
from bustedsolver import BustedSolver, BustedError

solver = BustedSolver("sk_live_your_key")

try:
    token = solver.solve("6Le...", "https://target.com", action="submit")
except BustedError as e:
    print(f"Failed: {e}")

# async
try:
    token = await solver.solve_async("6Le...", "https://target.com", action="submit")
except BustedError as e:
    print(f"Failed: {e}")
```

## Get API Key

Contact [@fkurmomslowly](https://t.me/fkurmomslowly) on Telegram for your `sk_live_` key.
