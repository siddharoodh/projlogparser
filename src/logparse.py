import heapq
import optparse
datafile = "data/data.txt"
import logging
import os 

handler = logging.StreamHandler()
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
LOGPARSER = logging.getLogger()
LOGPARSER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGPARSER.addHandler(handler)


class Logparser(object):
   def __init__(self):
      self.topn  = {}
      self.perc_success = {}
      self.perc_fail = {}
      self.tonN_unsuccess = {}
      self.topN_hosts = {}
      self.topN_sucess = {}
      self.counter = 0
      self.success = 0
      self.host_details = {}
      self.parse_log()

   def parse_log(self):
      """
      Parses http data sample log file and construct dict for
      each requests/data format based on condition
      """
      try:
         with open(datafile, "r+") as fd:
            data = fd.readlines()
      except Exception as ex:
         logging.exception ("Unable to open file")

      for line in data:
         try:
            fields = line.split()
            self.topn[fields[6]]  = self.topn.get(fields[6], 0) + 1
            status = fields[8]
            if not (int(status) >= 200 and int(status) < 400):
               self.tonN_unsuccess[fields[6]] = self.tonN_unsuccess.get(fields[6], 0)+1

            if int(status) >= 200 and int(status) < 400:
               self.topN_sucess[fields[6]] = self.topN_sucess.get(fields[6], 0)+ 1
               self.success = self.success + 1

            self.topN_hosts[fields[0]] = self.topN_hosts.get(fields[0], 0)+1
         
            if fields[0] in self.host_details:
               cnt = self.host_details[fields[0]]
               cnt[fields[6]] = cnt.get(fields[6], 0) + 1
               self.host_details[fields[0]] = cnt
            else:
               cnt = {}
               cnt[fields[6]] = cnt.get(fields[6], 0) + 1
               self.host_details[fields[0]] = cnt
          
         except Exception as ex:
            logging.exception("Does not have full content in line", str(ex))
         
         self.counter = self.counter + 1

   def get_top(self, n, dict_param):
      """ 
      Get the top n elements from give dict items
      param n: N elements
      dict_param: From dictionary to get the top elements
      return : return top N element from dict items
      """
      return heapq.nlargest(n, dict_param, key=dict_param.get)

   def get_topNhosts(self, topnhost):
       """
       Get the top n host page requests, and  return top n page requested in a host 
       param topnhost: pass topnhosts to get details
       return :
       """
       topval = self.get_top(topnhost, self.topN_hosts)
       for val in topval:
           print("Hosts : {}, number of requests made : {}".format(val, self.topN_hosts[val]))
           pages = self.get_top(5, self.host_details[val])
           for page in pages:
               logging.info("Page : {}, number of request for each : {}".format(page, self.host_details[val][page]))
            

   def get_topn(self, topn):
       """
       Get the top n pages request queried most
       param topn : topn number to fech page requests
       return:
       """
       topval = self.get_top(topn, self.topn)
       for val in topval:
           logging.info("Page : {}, number of request for each : {}".format(val, self.topn[val]))

   def get_percentage_success(self):
       """Get the percentage of succesful page requested"""
       logging.info("Percentage of successful requests: {}".format(float(self.success/self.counter)))
 
   def get_percentage_failure(self):   
       """Get the percentage of failure page requested"""
       logging.info("Percentage of Un - successful requests: {}".format(float((self.counter - self.success)/self.counter)))

   def get_topN_failure(self, topf):
       """
       Get the top n requested pages are failed
       param topf : topf number to fech failed page requests
       return:
       """
       topval = self.get_top(topf, self.tonN_unsuccess)
       for val in topval:
           logging.info("Page : {}, number of failure request  : {}".format(val, self.topn[val]))
        

def validate_options(parser, options):
   """
   Validate Only one option parameter is passed
   param: parser object
   options: options parameter
   return :
   """
   count = 0
   if options.topn:
      count = count + 1
   if options.perc_success:
      count = count + 1
   if options.perc_fail:
      count = count + 1
   if options.topnfail:
      count = count + 1
   if options.topnhost:
      count = count + 1
   
   if count == 1:
      return
   else:
      parser.error ("Please provide only one arguement option")


def main():
   """Main function to perform execution"""
   try:
       parser = optparse.OptionParser("logparse [--topn] [--perc_success] [--perc_fail] [--topnfail] [--topnhost]")
       parser.add_option('--topn', dest = 'topn',
                  type = 'int',
                  help = 'Top N requested pages')
       parser.add_option("--perc_success", action="store_true", dest="perc_success",
                  help=" Percentage of successful requested pages")
       parser.add_option("--perc_fail", action="store_true", dest="perc_fail",
                  help="Percentage of unsuccessful requested pages")
       parser.add_option("--topnfail", type = 'int', dest="topnfail",
                  help="Top N unsuccessful requestes pagess")
       parser.add_option("--topnhost", type = 'int', dest="topnhost",
                  help="The top N hosts making page request")

       (options, args) = parser.parse_args()
       validate_options(parser, options)

       obj = Logparser()
       if options.topn:
          obj.get_topn(options.topn)
       elif options.topnhost:
          obj.get_topNhosts(options.topnhost)
       elif options.perc_success:
          obj.get_percentage_success()
       elif options.perc_fail:
          obj.get_percentage_failure()
       elif options.topnfail:
          obj.get_topN_failure(options.topnfail)
       else:
          print("Nothing to process for this")

   except Exception as ex:
       logging.exception("Error Unable to execute Log Parser tool or invalid options are passed", str(ex))

if __name__ == "__main__":
    main()
