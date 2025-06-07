from setuptools import setup, find_packages

setup(
    name="famagent",
    version="0.1.0",
    description="🧠 FamAgent – Functional Assistant for Meaningful Research",
    author="Kaushal Wick",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "python-dotenv",
        "pydantic",
        "langchain",
        "langchain-community",
        "langchain-mistralai",
        # Include any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'famagent = famagent.main:main',
        ]
    },
    python_requires='>=3.10',
)
