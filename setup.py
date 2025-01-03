import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="holiday_predictor",
    version="1.0.0",
    author="azaz-az",
    author_email="a233d@outlook.com",
    description="一个预测中国的假期安排的小工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azaz-az/holiday-predictor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['zhdate'],
    keywords=['holiday', 'predictor', 'holiday_predictor', 'chinese_holiday']
)
