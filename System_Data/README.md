# Description
Retrive CPU, Memory, and Disk data and stores it into /tmp/system_data.json as JSON object. 

# Files 
`code/generate_system_data.py` - Generate data and store it into JSON file (under `/tmp`)

`code/test_generate_system_data.py` - pytest for `generate_system_data.py`

`sample/*.json` - JSON file with sample data 

# Example 
```
-- Execute 
ubuntu@ubuntu:~/foglamp-south-github$ python3 System_Data/code/generate_system_data.py
-- Output 
ubuntu@ubuntu:~/foglamp-south-plugin$ cat /tmp/system_data_2018_07_02_13_32_39.json | jq 
{
  "timestamp": "2018-07-02 13:32:39.043869",
  "asset": "system/cpu",
  "readings": {
    "iowait": 50.91,
    "idle": 11451.62,
    "system": 38.64,
    "cpu_0": 100
  },
  "key": "0ff01014-7e37-11e8-b893-0800275d93ce"
}
{
  "timestamp": "2018-07-02 13:32:39.043869",
  "asset": "system/memory",
  "readings": {
    "percent": 23.7
  },
  "key": "0ff01015-7e37-11e8-b893-0800275d93ce"
}
{
  "timestamp": "2018-07-02 13:32:39.043869",
  "asset": "system/disk",
  "readings": {
    "read": 19190,
    "warning": false,
    "useage": 27.9,
    "write": 14028
  },
  "key": "0ff01016-7e37-11e8-b893-0800275d93ce"
}
```