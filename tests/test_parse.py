import unittest
from mock import patch, mock_open, call, MagicMock, Mock
from src.logparse import main, Logparser

data = """216.244.66.230 - - [19/Dec/2020:14:14:26 +0100] GET /robots.txt HTTP/1.1 200 304 - Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)\n \
54.36.148.92 - - [19/Dec/2020:14:16:44 +0100] GET /robots.txt HTTP/1.1 200 30662 - Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/) -\n\
92.101.35.224 - - [19/Dec/2020:14:29:21 +0100] GET /administrator/index.php HTTP/1.1 200 4263  - Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322) -\n\
92.101.35.224 - - [19/Dec/2020:14:29:21 +0100] GET /administrator/index.php HTTP/1.1 200 4263  - Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322) -\n\
73.166.162.225 - - [19/Dec/2020:14:58:59 +0100] GET /apache-log/access.log HTTP/1.1 200 1299 - Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36 -\n\
73.166.162.225 - - [19/Dec/2020:14:58:59 +0100] GET /favicon.ico HTTP/1.1 404 217 http://www.almhuette-raith.at/apache-log/access.log Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36\n"""

class TestCollector(unittest.TestCase):

     @patch('builtins.open', new_callable=mock_open, read_data=data)
     def test_success_percent(self, mobj):
          obj = Logparser()
          self.assertEquals(float(obj.success/obj.counter), 0.8333333333333334)

     @patch('builtins.open', new_callable=mock_open, read_data=data)
     def test_success_failure(self, mobj):
          obj = Logparser()
          self.assertEquals(float((obj.counter - obj.success)/obj.counter), 0.16666666666666666)

     @patch('builtins.open', new_callable=mock_open, read_data=data)
     def test_topn(self, mobj):
          obj = Logparser()
          mockobj  = Mock()
          mockobj.return_value = Mock(return_value=['/robots.txt'])
          obj.get_top = mockobj
          obj.get_top.return_value = ['/robots.txt']
          obj.get_topn(1)
          val = '/robots.txt'
          self.assertEquals(obj.get_top.return_value[0], '/robots.txt')

     @patch('builtins.open', new_callable=mock_open, read_data=data)
     def test_topnfail(self, mobj):
          obj = Logparser()
          mockobj  = Mock()
          mockobj.return_value = Mock(return_value=['/favicon.ico'])
          obj.get_top = mockobj
          obj.get_top.return_value = ['/favicon.ico']
          obj.get_topN_failure(1)
          val = '/favicon.ico'
          self.assertEquals(obj.get_top.return_value[0], '/favicon.ico')
          

if __name__ == '__main__':
    unittest.main()
