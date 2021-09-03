## Studyportal-Utils
> This is a utility package built solely for managing studyportal developed by SDSLabs

Utility suite for deploying and managing [Studyportal](https://study.sdslabs.co/).

### Pre-requisites:
1. Python 3.6+ (preferred version: 3.6.9)
1. [PostgreSQL service](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04).

### Setup instructions:
1. Install [poetry](https://python-poetry.org/docs/#installation)
1. Generate a [credentials.json](https://developers.google.com/identity/protocols/oauth2/web-server) and place it in `studyportal-utils/studyportal`
1. Run ```poetry install``` to install the necessary packages.

### Usage instructions:
1. Run ```poetry shell``` to load into the poetry virtualenv
1. Inside the new shell, run ```studyportal --help``` to get the list of available commands.

Made with :heart: by [SDSLabs](https://sdslabs.co/)
