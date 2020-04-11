think about scale:

ndx + a <->  mdy + b
ignore plus / minus

ndx:
 n in 1-20
 x in 2,3,4,6,8,10,12,20


worst case 20d20: 20-400 (~400)
  -> 400*20*8 -> 64000


id, total, count
1d2, 1, 1
1d2, 2, 1
2d2, 2, 1
2d2, 3, 2
2d2, 4, 1
..

- stats:
- average roll (% of time)
- expect to get between (around 80% of the time)
- almost certain to get between (around 95% of the time)
- theortical min (%) & max (%)


method to compare 2 (in general symetric so clear winner) -> compare only 2 (overlay?)


script to populate table - method (iterate through)
-- populate with n=1 (range of values, count 1)
-- for n=1, running sum


- next level - kh / dl - could start with n<=4 in all combinations?
  -> script to populate all

new table -> details?

id, rolls, total, count
1d2 [1]
1d2 [2]
2d2 [1,1], 2, 1
2d2 [1,2], 3, 2
2d2 [2,2], 4, 1
..


-> validation khx or dlx - n should be lower than total
id, total, count
2d2kh1 1, 1
2d2kh1 2, 3
2d2kl1 1, 3
2d2kl1 2, 1
...

Need a query parser prob (remove spaces, un-caps, map kh to kh1 etc)



- https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc
- https://gist.github.com/mayukh18/2223bc8fc152631205abd7cbf1efdd41/
- https://medium.com/@pemagrg/build-a-web-app-using-pythons-flask-for-beginners-f28315256893
