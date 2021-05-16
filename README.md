# Sample Http response data log parser
Using the sample http log file, perform the following tasks:
1. Top 10 requested pages and the number of requests made for each
2. Percentage of successful requests (anything in the 200s and 300s range)
3. Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
4. Top 10 unsuccessful page requests
5. The top 10 hosts making the most requests, displaying the IP address and number of requests made.
6. Option parsing to produce only the report for one of the previous points (e.g. only the top 10 urls, only the percentage of successful requests and so on)

# Requirments:
Steps to create Virtual environment
- python3 -m venv logparser
- source logparser/bin/activate

Install packages
- pip install -r requirements.txt

# How to use
Tool is to read the data.txt log file, and process/construct the report based on input parameter options
1. Download source code from git report 
2. (Pre-req) : Require requirements steps before executing steps
3. set PYTHONPATH to directory you downloaded (e.g : export PATHONPATH=~/.projlogparser)
4. Execute the script
   Source can run in same $HOME/projlogparser directory
  - $python src/logparse.py 
  - Usage: logparse [--topn] [--perc_success] [--perc_fail] [--topnfail] [--topnhost]

5. Output of tool will shows on output console
   eg:-
    $> python src/logparse.py --topn 4 
    INFO:root:Page : /index.php?option=com_contact&view=contact&id=1, number of request for each : 10819
    INFO:root:Page : /administrator/index.php, number of request for each : 239
    INFO:root:Page : /, number of request for each : 204
    INFO:root:Page : /apache-log/access.log, number of request for each : 128
    
# Examples
  1. % python src/logparse.py --help  
    Usage: logparse [--topn] [--perc_success] [--perc_fail] [--topnfail] [--topnhost]

    Options:
    -h, --help           show this help message and exit
    --topn=TOPN          Top N requested pages
    --perc_success        Percentage of successful requested pages
    --perc_fail          Percentage of unsuccessful requested pages
    --topnfail=TOPNFAIL  Top N unsuccessful requestes pagess
    --topnhost=TOPNHOST  The top N hosts making page request
  2. % python src/logparse.py --topn 4
    Shows top N pages requests are made.
    INFO:root:Page : /index.php?option=com_contact&view=contact&id=1, number of request for each : 10819
    INFO:root:Page : /administrator/index.php, number of request for each : 239 
    INFO:root:Page : /, number of request for each : 204
    INFO:root:Page : /apache-log/access.log, number of request for each : 128
  3.  % python src/logparse.py --topnfail 4
    Shows ton N page requests failed
    INFO:root:Page : /favicon.ico, number of failure request  : 57
    INFO:root:Page : /templates/_system/css/general.css, number of failure request  : 52
    INFO:root:Page : /index.php?option=com_easyblog&view=dashboard&layout=write, number of failure request  : 43
    INFO:root:Page : /icons/blank.gif, number of failure request  : 5
  4. % python src/logparse.py --perc_success  
    Shows percentage of page requests are success
    INFO:root:Percentage of successful requests: 0.9767404426559356
  5. % python src/logparse.py --perc_fail    
     Shows percentage of page requests failed
     INFO:root:Percentage of Un - successful requests: 0.023259557344064385
  6.  % python src/logparse.py --topnhost 4   
     Will report ton n host and number of requests made, and for each host top n page requests made.
     Hosts : 176.222.58.254, number of requests made : 656
     INFO:root:Page : /index.php?option=com_contact&view=contact&id=1, number of request for each : 656
     Hosts : 45.144.0.179, number of requests made : 630.
     INFO:root:Page : /index.php?option=com_contact&view=contact&id=1, number of request for each : 630
     Hosts : 176.222.58.90, number of requests made : 600 
     INFO:root:Page : /index.php?option=com_contact&view=contact&id=1, number of request for each : 600
     Hosts : 45.153.227.31, number of requests made : 598
     INFO:root:Page : /index.php?option=com_contact&view=contact&id=1, number of request for each : 598
     
 # Testing
   Test code can run in same $HOME/projlogparser directory
  % python -m unittest tests/test_parse.py

   Added unit test cases for all the possible cases and validate with different paremeters
   
Note : Script can execute either both python/python3.8
