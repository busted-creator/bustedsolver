from setuptools import setup, find_packages

setup(
    name="bustedsolver",
    version="1.3.0",
    description="reCAPTCHA v3 Solver SDK",
    packages=find_packages(),
    install_requires=["httpx"],
    python_requires=">=3.8",
)
