from setuptools import setup, find_packages

setup(
    name="fastapi_zitadel_auth",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "httpx",
    ],  # Ensure to list all your dependencies
    author="Kevin Oliveira",
    author_email="kevinols08@gmail.com",
    description="Utilitário FastAPI para autenticação com Zitadel",
)