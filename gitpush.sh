git commit -a -m "modify"
git push heroku master
heroku ps:scale web=1
heroku open
