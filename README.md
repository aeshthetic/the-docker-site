# The Docker
## Setting up an environment
Unsurprisingly, the Docker site uses docker. To
set up a dev environment for the site, you should
install Docker in whichever way your OS/distribution
is required to. You will also need to install Docker Compose which can be done via python3-pip (`pip3 install docker-compose`).

After installing these, ensure that you've created a valid .env file in the root of the project. The repository contains an example of what the file should look like.

At this point, you should be able to run `docker-compose build` and `docker-compose up`, optionally running the latter with the `-d` flag to run
the app in a detached state. If you choose to do so, you may use `docker-compose logs` to view what you would have seen had you not run it with `-d`.

In order to initialize the database, run
`docker-compose run web bash`, which will give you access to a shell for the container. Once in this shell, run `python create_db.py` to initialize the database tables.
After this, you may use ^d or `exit` to leave the shell, and may need to use ^c to restore your regular shell.
This is a redundant and inefficient method of handling migrations and will be changed in the future. However, at this point you should be able to visit the site at `localhost`.

If you simply wish to work on html/css, the experimental directory contains valid html and css for local testing without docker.
