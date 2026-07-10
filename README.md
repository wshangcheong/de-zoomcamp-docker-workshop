# de-zoomcamp-docker-workshop

## how this mini program generally works
1. just to get a taste of docker
2. run `pip install uv` in terminal
3. run `uv init --python=3.13` (or some other python version) to create virtual environment (.venv) as well as pyproject.toml file so keep package requirements
4. run `uv add pandas pyarrow` in terminal will add these packages to the .toml file
2. run `docker compose up` to get things running, i.e. setup db, postgres interface, and run ingestion of taxi data
3. follow steps [here](https://github.com/wshangcheong/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/07-pgadmin.md#connect-pgadmin-to-postgresql) to check out the postgres db and run some sql stuff there
4. follow steps [here](https://github.com/wshangcheong/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/11-cleanup.md#cleanup) to clean up after we're all done

## Notes to self: 
- important things would be docker file and docker compose yaml  
- docker file carries instructions for image  
- docker compose contains overall instructions to manage multiple docker containers  
- volumes allow the docker images to store data so they can be reaccessed the next time we connect to them
- caching happens so steps may be skipped when dockerfile or docker-compose runs
- make force builds explicit if something's changed and should be shown. maybe versioning comes in play here?
- uv handles env requirements .toml and uv.lock should get copied over and run first in docker file
- `pip install uv` > `uv init xx` > `uv add x1 x2 x3...` > `uv run python filename.py *args`
- add things to .gitignore, e.g. data files or credentials, to not have them committed to git 
- networks in docker help containers communicate with each other
- still don't fully get ports but we'll get there some day
- docker {thing to clear} prune command to clear things up

## some questions remain:
- file structure? where to keep dockerfile? can I have multiple in separate folders? 
- can there only be one docker-compose? (based on the way they're named, probably not...)