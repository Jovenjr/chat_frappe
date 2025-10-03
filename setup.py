from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chat_frappe",
    version="0.0.1",
    author="Your Company",
    author_email="info@yourcompany.com",
    description="Sistema de chat con agentes IA para Frappe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jovenjr/chat_frappe",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        # frappe is installed and managed by bench
    ],
    include_package_data=True,
    zip_safe=False,
)
