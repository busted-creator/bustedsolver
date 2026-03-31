# BustedSolver

Fast reCAPTCHA v3 solver API.

> Currently in early access. More features coming soon.

## Install

```
pip install git+https://github.com/busted-creator/bustedsolver.git
```

## Usage

```python
from bustedsolver import BustedSolver

solver = BustedSolver("sk_live_your_key_here")

# solve reCAPTCHA v3
token = solver.solve(
    site_key="6Le...",           # reCAPTCHA site key from target page
    page_url="https://...",      # URL of page with reCAPTCHA
    action="submit",             # action string (default: "submit")
)

# use token in your requests
payload = {
    "g-recaptcha-response": token,
}
```

## Find reCAPTCHA Info

Open target page source and search for:
- **site_key**: Search `render=` or `sitekey` (starts with `6L`)
- **action**: Search `grecaptcha.execute` (inside `{action: 'xxx'}`)
- **page_url**: The page URL

## Check Usage

```python
usage = solver.usage()
print(f"Used: {usage['requests_used']}/{usage['requests_limit']}")
```

## Error Handling

```python
from bustedsolver import BustedSolver, BustedError

solver = BustedSolver("sk_live_your_key")

try:
    token = solver.solve("6Le...", "https://target.com", action="submit")
except BustedError as e:
    print(f"Failed: {e}")
```

## Note

BustedSolver does NOT need a proxy. It connects directly to our API. Do not set HTTP_PROXY/HTTPS_PROXY environment variables when using BustedSolver.

## Get API Key

Contact [@fkurmomslowly](https://t.me/fkurmomslowly) on Telegram for your `sk_live_` key.
