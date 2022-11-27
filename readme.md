# Software Engineering Project

# Instalation
## Dependcies
Install:

* Git           [installaation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Docker [installation](https://docs.docker.com/get-docker/)
* Docker Compose [installation](https://docs.docker.com/compose/install/)

## Download repository

`git clone https://github.com/Software-eng-group-3/Project.git`

## Setup
Setup and run the docker continers:

Build the contianers (takes a while)
`docker-compose up --build`
should only need to build once after that relaunch

visit `http://localhost:3000/test` 
If you can see the list of names the development environment is working properly

Close the continers `ctl-c`

relaunch the containers without building `docker-compose up`

### Reset
If everything stops working try the following

1. purge everything `docker system prune -a`
2. Rebuild with the previous commands

If that does not work

3. Pull from the master branch
4. Purge and relaunch



# Making Changes
For this recomend a GIU version of git Git Desktop or the one included in VS code

when adding a new feature

1. pull the master branch
2. make a new branch for the feature
3. Create the feature
4. Reguarly create commits for any element of significance <- easier to track if there are many
   1. If stopping development for a bit remenber to forch push your branch to github <- prevents data loss
5. Once complete
6. Re-pull the master branch
7. Merge your branch to the master
8. resolve any coflicts
9. Submit a pull request with the new master, wait for a review

If you are unsure ask on discord or use some google-fu

# Postgress
Database IDs
| | |
|-|-|
|System   | `PostgreSQL` |
|Server   | `db`         |
|username | `postgres`   |
|password | `admin`      |
|databse  | `development`|

### adminer
Primary interaction with the database use adminer
[localhost:8080](http://localhost:8080)

This should hopefully be fairly easy
(It came packaged with the postgreSQL server)

### terminal
requres psql: [installation](https://blog.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/)

run `psql postgresql://postgres:admin@localhost:5432/development`

### Schema

the `./postgres/schema.sql` file is run only on `--build` and not at any other time.

All other `.sql` files in the folder are ingored copy them to `/docker-entrypoint-initdb.d/` using the docker file to include them

# Python 

program should re-run on saving file

No notes yet

# nodejs, bootstrap, react

program should re-run on saving file

No notes yet





# Tutorials
Usefull tutorials I have found on the technologies being used

Please add any tutorials you feel are usefull

## Docker
https://blog.atulr.com/docker-local-environment/

`docker exec -it <container> bash`

## Python

### PostgreSQL and Python 

https://www.postgresqltutorial.com/postgresql-python/

### Json and Python

https://realpython.com/python-json/

### Flask


## Front end
### React
https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
https://www.digitalocean.com/community/tutorials/how-to-call-web-apis-with-the-useeffect-hook-in-react
### Bootstrap


### Other

https://www.velotio.com/engineering-blog/how-to-implement-server-sent-events-using-python-flask-and-react
