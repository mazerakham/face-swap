from setuptools import setup, find_packages

setup(
    name="face_swap",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "httpx>=0.25.1",
        "pydantic>=2.5.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pyright>=1.1.335",
            "black>=23.11.0",
        ]
    },
    python_requires=">=3.11",
)
