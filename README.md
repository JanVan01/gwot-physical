# GWOT Physical Smart Device

## Installation

Currently tested using Raspbian only.

To install it download these files as ZIP file or get them using git. 

Give the file setup/setup.sh rights to be executable:

`sudo chmod +x setup/setup.sh`

Afterwards execute the setup and as arguments specify the desired database name (here: `data`) and a database password for PostgreSQL (here: `myS3cretP@ssword`), e.g.:

`sudo setup/setup.sh data myS3cretP@ssword`
