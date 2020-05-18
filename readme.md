# Dice Stats

An experimental site that was hastily built during Covid-19 quarantine as a learning project.

See: https://dice-stats.herokuapp.com/

Feel free to add issues (or pull requests)

---

### Development:

##### docker build command:
`docker-compose up --build --force-recreate`

##### Known issues / Work in progress:

1. Handle r<1 and ro<1 type rolls
2. Better error handling and more useful error messages / validation
3. Improve chart
  - vertical lines eg for average
  - better represent specific points - dots and hover?
4. Improve responsiveness / mobile


##### Tech stack

- Heroku + Docker
- Postgres
- Flask
- Bootstap + D3


##### Useful links for future reference

- https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc
- https://gist.github.com/mayukh18/2223bc8fc152631205abd7cbf1efdd41/
- https://medium.com/@pemagrg/build-a-web-app-using-pythons-flask-for-beginners-f28315256893


- https://devcenter.heroku.com/articles/build-docker-images-heroku-yml
- https://rominirani.com/docker-tutorial-series-a7e6ff90a023
- https://medium.com/@hmajid2301/implementing-sqlalchemy-with-docker-cb223a8296de
- https://towardsdatascience.com/learn-enough-docker-to-be-useful-b7ba70caeb4b
- https://www.databaselabs.io/help/tutorials/setting-up-flask-sqlalchemy-postgres
