from setuptools import find_packages, setup

setup(
    name="genai_4_dps_helper",
    version="0.2.6",
    packages=find_packages(),
    install_requires=[
        # List any dependencies your library needs
        "pandas==2.1.4",
        "ibm_watsonx_ai==1.2.1",
        "pymilvus==2.5.3",
        "pydantic==2.10.5",
        "setuptools>=73.0",
        "pymupdf==1.25.2",
    ],
    description="A common library for reusable and repeated code for the GenAI4DPS Training Courses .",
    author="Benjamin Janes",
    author_email="benjamin.janes@se.ibm.com",
)
