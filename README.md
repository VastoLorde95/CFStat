# CFStat
A Python module that allows you to perform statistical analysis of your performance on Codeforces. The module provides three main functions:

1. `compareUsers`: Returns a list of all problems that have been solved by you but not by another user
2. `getSubmissions`: Returns a list of all your submissions over a specific number of pages.
3. `getWeeklyStatistics` : Tabulates all your submission statistics for each week - reports your acceptance rate, what errors were committed etc

Requirements:
1. Python 2.7.x
2. Beautiful Soup
3. requests
4. tabulate

Implmentation Details:

  The date time objects are converted to isocalendar format.
  
  `start_year` is the year starting from which you want to fetch submissions
  
  `end_year` is the year till when you want to fetch submissions
  
  The arguments of getSubmissions are as follows
  
  1. `user` = codeforces username
  2. `page_mx` = the maximum number of submission pages you want to anaylze. If you give a number that is greater than the
  number of submission pages a user has, then you will get incorrect statisitcs due to overcounting.
  3. `print_flag` = say False if you dont want the program to print your submission verdicts (desirable if you have lots of submissions!)
    
Please refer `example.py` to learn how to use this module.
