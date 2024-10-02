from setuptools import find_packages, setup

setup(
    name="google_calendar_utils",
    version="0.1",
    packages=find_packages(),
    install_requires=["google_auth_oauthlib", "google-api-python-client"],
    url="https://github.com/cm-hirano-shigetoshi/google-calendar-utils",
    author="cm-hirano.shigetoshi",
    author_email="hirano.shigetoshi@classmethod.jp",
    description="GoogleCalendarClass",
)
