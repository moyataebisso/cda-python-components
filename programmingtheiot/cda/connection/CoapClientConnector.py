#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging

from coapthon.client.helperclient import HelperClient
from coapthon import defines

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

class CoapClientConnector(IRequestResponseClient):
    """
    CoAP client connector implementation using CoAPthon3 library.
    Sends requests to the GDA's CoAP server.
    """
    
    def __init__(self, host: str = None):
        """
        Initializes the CoAP client connector.
        
        @param host The host address (optional, will read from config if not provided)
        """
        self.config = ConfigUtil()
        self.dataMsgListener = None
        
        # Load configuration
        if host:
            self.host = host
        else:
            self.host = self.config.getProperty(
                ConfigConst.COAP_GATEWAY_SERVICE, 
                ConfigConst.HOST_KEY, 
                ConfigConst.DEFAULT_HOST
            )
        
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE,
            ConfigConst.PORT_KEY,
            ConfigConst.DEFAULT_COAP_PORT
        )
        
     #   self.enableConfirmedMsgs = self.config.getBoolean(
      #      ConfigConst.COAP_GATEWAY_SERVICE,
       #     ConfigConst.ENABLE_CONFIRMED_MSGS_KEY
        #)
        self.enableConfirmedMsgs = True
        # Build the server URL
        self.url = f"coap://{self.host}:{self.port}"
        
        logging.info(f"CoAP Client will connect to: {self.url}")
        
        self._initClient()
    
    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a discovery request to find available resources on the CoAP server.
        
        @param timeout Timeout in seconds
        @return True on success, False otherwise
        """
        logging.info(f"Discovering remote resources at: {self.url}")
        
        try:
            client = HelperClient(server=(self.host, self.port))
            response = client.discover(timeout=timeout)
            
            if response:
                logging.info(f"Discovery response: {response.pretty_print()}")
                return True
            else:
                logging.warning("No discovery response received")
                return False
                
        except Exception as e:
            logging.error(f"Failed to discover resources: {e}")
            return False
        finally:
            if client:
                client.stop()
    
    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, 
                         enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a DELETE request to the specified resource.
        
        @param resource The resource enum
        @param name Optional resource name
        @param enableCON Enable confirmed messaging
        @param timeout Timeout in seconds
        @return True on success, False otherwise
        """
        if not resource:
            logging.warning("No resource specified for DELETE request")
            return False
        
        resourcePath = resource.value
        url = f"{self.url}/{resourcePath}"
        
        logging.info(f"Sending DELETE request to: {url}")
        
        try:
            client = HelperClient(server=(self.host, self.port))
            response = client.delete(resourcePath, timeout=timeout)
            
            if response:
                logging.info(f"DELETE response code: {response.code}")
                self._handleResponse(response, resource)
                return True
            else:
                logging.warning("No DELETE response received")
                return False
                
        except Exception as e:
            logging.error(f"Failed to send DELETE request: {e}")
            return False
        finally:
            if client:
                client.stop()
    
    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None,
                      enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a GET request to the specified resource.
        
        @param resource The resource enum
        @param name Optional resource name
        @param enableCON Enable confirmed messaging
        @param timeout Timeout in seconds
        @return True on success, False otherwise
        """
        if not resource:
            logging.warning("No resource specified for GET request")
            return False
        
        resourcePath = resource.value
        url = f"{self.url}/{resourcePath}"
        
        logging.info(f"Sending GET request to: {url}")
        
        try:
            client = HelperClient(server=(self.host, self.port))
            response = client.get(resourcePath, timeout=timeout)
            
            if response:
                logging.info(f"GET response code: {response.code}")
                logging.info(f"GET response payload: {response.payload}")
                self._handleResponse(response, resource)
                return True
            else:
                logging.warning("No GET response received")
                return False
                
        except Exception as e:
            logging.error(f"Failed to send GET request: {e}")
            return False
        finally:
            if client:
                client.stop()
    
    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None,
                       enableCON: bool = False, payload: str = None, 
                       timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a POST request with payload to the specified resource.
        
        @param resource The resource enum
        @param name Optional resource name
        @param enableCON Enable confirmed messaging
        @param payload The payload string to send
        @param timeout Timeout in seconds
        @return True on success, False otherwise
        """
        if not resource:
            logging.warning("No resource specified for POST request")
            return False
        
        resourcePath = resource.value
        url = f"{self.url}/{resourcePath}"
        
        logging.info(f"Sending POST request to: {url}")
        
        try:
            client = HelperClient(server=(self.host, self.port))
            response = client.post(resourcePath, payload, timeout=timeout)
            
            if response:
                logging.info(f"POST response code: {response.code}")
                self._handleResponse(response, resource)
                return True
            else:
                logging.warning("No POST response received")
                return False
                
        except Exception as e:
            logging.error(f"Failed to send POST request: {e}")
            return False
        finally:
            if client:
                client.stop()
    
    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None,
                      enableCON: bool = False, payload: str = None,
                      timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a PUT request with payload to the specified resource.
        
        @param resource The resource enum
        @param name Optional resource name
        @param enableCON Enable confirmed messaging
        @param payload The payload string to send
        @param timeout Timeout in seconds
        @return True on success, False otherwise
        """
        if not resource:
            logging.warning("No resource specified for PUT request")
            return False
        
        resourcePath = resource.value
        url = f"{self.url}/{resourcePath}"
        
        logging.info(f"Sending PUT request to: {url}")
        
        try:
            client = HelperClient(server=(self.host, self.port))
            response = client.put(resourcePath, payload, timeout=timeout)
            
            if response:
                logging.info(f"PUT response code: {response.code}")
                self._handleResponse(response, resource)
                return True
            else:
                logging.warning("No PUT response received")
                return False
                
        except Exception as e:
            logging.error(f"Failed to send PUT request: {e}")
            return False
        finally:
            if client:
                client.stop()
    
    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        """
        Sets the data message listener for handling responses.
        
        @param listener The listener instance
        @return True on success, False otherwise
        """
        if listener:
            self.dataMsgListener = listener
            logging.info("Data message listener set")
            return True
        else:
            logging.warning("No data message listener provided")
            return False
    
    def startObserver(self, resource: ResourceNameEnum = None, name: str = None,
                     ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        """
        Starts observing a resource for changes.
        
        @param resource The resource enum
        @param name Optional resource name
        @param ttl Time to live in seconds
        @return True on success, False otherwise
        """
        if not resource:
            logging.warning("No resource specified for observation")
            return False
        
        resourcePath = resource.value
        logging.info(f"Starting observation of resource: {resourcePath}")
        
        # Note: CoAPthon3 observe implementation would go here
        # This is a placeholder for the basic implementation
        logging.warning("Observer functionality not fully implemented")
        return False
    
    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None,
                    timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Stops observing a resource.
        
        @param resource The resource enum
        @param name Optional resource name
        @param timeout Timeout in seconds
        @return True on success, False otherwise
        """
        if not resource:
            logging.warning("No resource specified to stop observation")
            return False
        
        resourcePath = resource.value
        logging.info(f"Stopping observation of resource: {resourcePath}")
        
        # Note: CoAPthon3 observe implementation would go here
        logging.warning("Observer functionality not fully implemented")
        return False
    
    def _initClient(self):
        """
        Initializes the CoAP client (placeholder for any initialization needed).
        """
        logging.info("CoAP client connector initialized")
    
    def _handleResponse(self, response, resource: ResourceNameEnum):
        """
        Handles the CoAP response and notifies the data message listener.
        
        @param response The CoAP response object
        @param resource The resource that was accessed
        """
        if response and self.dataMsgListener:
            payload = response.payload
            if payload:
                # Notify the listener with the response
                self.dataMsgListener.handleIncomingMessage(resource, payload)
