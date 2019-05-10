import copy
import uuid
import logging
import math

from foglamp.common import logger
from foglamp.plugins.common import utils
from foglamp.services.south import exceptions

from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.HumiditySensor import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *


__author__ = "Ori Shadmon"
__copyright__ = "Copyright (c) 2019 Dianomic Systems"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_DEFAULT_CONFIG = {
} 

def plugin_init(config):
   """ Initialise the plugin.
   Args:
      config: JSON configuration document for the South plugin configuration category
   Returns:
      data: JSON object to be used in future calls to the plugin
   Raises:
   """
   try: 
      data = copy.deepcopy(config) 
      """ For each sensor add: 
         - Init 
         - setDeviceSerialNumber
         - setHubPort
         - .setIsHubPortDevice
         - .setChannel
      """ 
      # humidity 
      data['humidity'] = HumiditySensor()
      data['humidity'].setDeviceSerialNumber(561266)
      data['humidity'].setHubPort(5)
      data['humidity'].setIsHubPortDevice(False)
      data['humidity'].setChannel(0)

      # temperature 
      data['temp'] = TemperatureSensor()
      data['temp'].setDeviceSerialNumber(561266)
      data['temp'].setHubPort(5)
      data['temp'].setIsHubPortDevice(False)
      data'[temp'].setChannel(0)

      # Current 
      data['current'] = CurrentInput()
      data['current'].setDeviceSerialNumber(561266)
      data['current'].setHubPort(3)
      data['current'].setIsHubPortDevice(False)
      data['current'].setChannel(0)

      # for each sensor do try/catch (pass) on the first get
      data['humidity'].openWaitForAttachment(5000)
      try: 
         data['humidity'].getHumidity()
      except Exception as e:
         pass 

      data['temp'].openWaitForAttachment(5000)
      try:
         data['temp'].getTemperature()
      except Exception as e:
         pass

      data['current'].openWaitForAttachment(5000)
      try: 
         ch.getCurrent()
      except Exception as e: 
         pass 

   except Exception as e: 
      _LOGGER.exception("SLTC exception: {}".format(str(ex)))
      raise ex 
   return data 

def plugin_pull(handle): 
   """ Extract data from sensors and return in a JSON document as a Python dict. 
       Available for poll-mode only. 
   Args: 
      handle: returns pluin initialisation call 
   Returns: 
      sensor readings ina  JSON document, as a Python dict; if available. Otherwise returns None
   Raises: 
      TimeoutError 
   """ 
   try: 
      timestamp = utils.local_timestamp()
      data = list()
      """ Append each sensor to data list
         - asset (name) 
         - timestamp 
         - key 
         -readings {} 
      """ 
      data.append({
         'asset': 'temperature_and_humidity', 
         'timestamp': timestamp,
         'key': str(uuid.uuid4()), 
         'readings': { 
            "humidity": data['humidity'].getHumidity(), 
            "temperature": data['temp'].getTemperature()
         }
      })

      data.append({
         'asset': 'current_input', 
         'timestamp': timestamp, 
         'key': str(uuid.uuid4())
         'readings': { 
            "current_input": data['current'].getCurrent() 
         }
      }) 

   except (Exception, RuntimeError) as ex:
      _LOGGER.exception("SLTC exception: {}".format(str(ex)))
      raise exceptions.DataRetrievalError(ex)
   else: 
      return data 

def plugin_reconfigure(handle, new_config):
   """ Reconfigures the plugin
   Args:
       handle: handle returned by the plugin initialisation call
       new_config: JSON object representing the new configuration category for the category
   Returns:
       new_handle: new handle to be used in the future calls
   """
   _LOGGER.info("Old config for SLTC plugin {} \n new config {}".format(handle, new_config))
   new_handle = copy.deepcopy(new_config)
   return new_handle


def plugin_shutdown(handle):
   """ Shutdowns the plugin doing required cleanup, to be called prior to the South plugin service being shut down.
   Args:
       handle: handle returned by the plugin initialisation call
   Returns:
       plugin shutdown
   """
   _LOGGER.info('SLTC plugin shut down.')
