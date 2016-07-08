# CFStat
A web scraping tool that allows you to perform statistical analysis of your performance on Codeforces

Requirements:
1. Python 2.7.x
2. Beautiful Soup
3. requests
4. tabulate

Implmentation Details:
  The date time objects are converted to isocalendar format.
  
  'start_year' is the year starting from which you want to fetch submissions
  'end_year' is the year till when you want to fetch submissions
  
  The arguments of getSubmissions are as follows:
    user = codeforces username
    page_mx = the maximum number of submission pages you want to anaylze. If you give a number that is greater than the 
    number of submission pages a user has, then you will get incorrect statisitcs due to overcounting.
    print_flag = say False if you dont want the program to print your submission verdicts (desirable if you have lots of submissions!)
    
