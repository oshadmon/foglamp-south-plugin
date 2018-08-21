import datetime 
import os 
import queue 
import random
import requests
import threading
import uuid

import generate_github_data

class TestGitHubData: 
   def setup_method(self): 
      """
      Given authentication file (auth_pair.txt), prepare config information
      Note that auth_pair should be under $HOME and with valid info for tests to succeed.
      :param: 
         self.auth - user:password of GitHub 
         self.repo - repo testing against 
         self.org - organization repo is under 
         self.json_dir - dir to store JSON data 
      """
      env=os.path.expanduser(os.path.expandvars('$HOME/auth_pair.txt'))
      with open(env, 'r') as f:
         output=f.read().replace('\n', '').split(' ') 
      self.auth=(str(output[0].split(':')[0]), str(output[0].split(':')[-1]))
      self.repo=output[1]
      self.org=output[2] 
      self.json_dir=output[3]

      os.system('rm -rf %s/*.json' % self.json_dir)

   def teardown_method(self): 
      """
      Remove data in self.json_dir
      """
      os.system('rm -rf %s/*.json') 

   def __main(self, process:str='traffic')->(requests.models.Response, str):
      """
      Execute "main" like behavior for get_timestamp, send_request to simply testing. 
      :param: 
         process:str - process you want to return (traffic, commits, clones)
      :return:
         timestamp (str) and requests.models.Response based on process
      """
      timestamp_que=queue.Queue()
      traffic_que=queue.Queue()
      commits_que=queue.Queue()
      clones_que=queue.Queue()
      threads=[threading.Thread(target=generate_github_data.get_timestamp, args=(timestamp_que,)),
               threading.Thread(target=generate_github_data.send_request,  args=(traffic_que, commits_que, clones_que, self.repo, self.org, self.auth,))
              ]
   
      for thread in threads:
         thread.start()
      for thread in threads:
         thread.join()
      timestamp=timestamp_que.get()
      traffic_request=traffic_que.get()
      commits_request=commits_que.get()
      clones_request=clones_que.get()

      if process.lower() == 'traffic': 
         return traffic_request, timestamp
      if process.lower() == 'commits': 
         return commits_request, timestamp
      if process.lower() == 'clones': 
         return clones_request, timestamp

   def test_get_timestamp(self): 
      """
      Test get_timestamp method
      :assert: 
         Method returns today's date formated as %Y_%m_%d
      """
      que=queue.Queue() 
      generate_github_data.get_timestamp(que)
      timestamp=que.get()
      assert timestamp == datetime.datetime.now().strftime('%Y_%m_%d')

   def test_send_request(self): 
      """
      Test send_requests
      :assert: 
         Method retrives valid status codes
      """
      traffic_que=queue.Queue()
      commits_que=queue.Queue()
      clones_que=queue.Queue()

      generate_github_data.send_request(traffic_que, commits_que, clones_que, self.repo, self.org, self.auth)

      traffic=traffic_que.get()
      commits=commits_que.get()
      clones=clones_que.get()
      
      for code in [traffic.status_code, commits.status_code, clones.status_code]:
         assert code == 200


   def test_read_traffic(self): 
      """
      Test read_traffic 
      :assert:
         1. returns a list 
         2. a random set in list is dictionary with valid data
      """
      traffic_request, timestamp = self.__main('traffic')
      data=generate_github_data.read_traffic(traffic_request, self.repo, timestamp)
      assert type(data) == list
      data_set=random.choice(data)
      assert type(data_set) == dict
      assert sorted(data_set.keys()) == ['asset', 'key', 'readings', 'timestamp']
      assert data_set['asset'] == 'github/FogLAMP/traffic' 
      assert list(data_set['readings'].keys()) == ['traffic']
      try:
         uuid.UUID(data_set['key'], version=4)
      except:
         return False

   def test_read_commits_timestamp(self): 
      """
      Test read_commits_timestamp
      :assert: 
         1. returns a list 
         2. a random set in list is dictiionary with valid data 
      """
      commits_request, timestamp = self.__main('commits')
      data=generate_github_data.read_commits_timestamp(commits_request, self.repo, timestamp)
      assert type(data) == list
      data_set=random.choice(data)
      assert type(data_set) == dict 
      assert sorted(data_set.keys()) == ['asset', 'key', 'readings', 'timestamp']
      assert data_set['asset'] == 'github/FogLAMP/commits/timestamp' 
      assert list(data_set['readings'].keys()) == ['commits/timestamp']
      try:
         uuid.UUID(data_set['key'], version=4)
      except:
         return False


