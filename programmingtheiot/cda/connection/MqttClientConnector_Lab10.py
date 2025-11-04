#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging
import ssl
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

class MqttClientConnector(IPubSubClient):
    """
    Lab Module 10 - Enhanced with TLS support (PIOT-CDA-10-001)
    """
    
    def __init__(self, clientID: str = None, enableTls: bool = False, enablePerformanceTest: bool = False):
        """
        Default constructor with TLS support for Lab Module 10
        
        @param clientID Unique client identifier
        @param enableTls Enable TLS/SSL encryption
        @param enablePerformanceTest Disable verbose logging for performance tests
        """
        self.config = ConfigUtil()
        self.dataMsgListener = None
        self.enableTls = enableTls
        self.enablePerformanceTest = enablePerformanceTest
        
        self.host = \
            self.config.getProperty( \
                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
        
        if self.enableTls:
            self.port = \
                self.config.getInteger( \
                    ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.SECURE_PORT_KEY, ConfigConst.DEFAULT_MQTT_SECURE_PORT)
        else:
            self.port = \
                self.config.getInteger( \
                    ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
        
        self.keepAlive = \
            self.config.getInteger( \
                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
        
        self.defaultQos = \
            self.config.getInteger( \
                ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
        
        self.mqttClient = None
        
        if not clientID:
            clientID = 'CDAMqttClientID001'
            
        self.clientID = clientID
            
        logging.info('\tMQTT Client ID:   ' + self.clientID)
        logging.info('\tMQTT Broker Host: ' + self.host)
        logging.info('\tMQTT Broker Port: ' + str(self.port))
        logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
        if self.enableTls:
            logging.info('\tMQTT TLS Enabled: True')
    
    def configureTls(self):
        """Configure TLS/SSL settings for secure connection"""
        try:
            ca_cert_path = "config/cert/ca.crt"
            
            self.mqttClient.tls_set(
                ca_certs=ca_cert_path,
                certfile=None,
                keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None
            )
            
            self.mqttClient.tls_insecure_set(True)
            
            logging.info('TLS configuration completed successfully')
            
        except Exception as e:
            logging.error('Failed to configure TLS: %s', e)
    
    def connectClient(self) -> bool:
        if not self.mqttClient:
            self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = True)
            
            if self.enableTls:
                self.configureTls()
            
            self.mqttClient.on_connect = self.onConnect
            self.mqttClient.on_disconnect = self.onDisconnect
            self.mqttClient.on_message = self.onMessage
            self.mqttClient.on_publish = self.onPublish
            self.mqttClient.on_subscribe = self.onSubscribe
        
        if not self.mqttClient.is_connected():
            logging.info('MQTT client connecting to broker at host: ' + self.host)
            self.mqttClient.connect(self.host, self.port, self.keepAlive)
            self.mqttClient.loop_start()
            
            return True
        else:
            logging.warning('MQTT client already connected. Ignoring connect request.')
            
            return False
    
    def disconnectClient(self) -> bool:
        if self.mqttClient and self.mqttClient.is_connected():
            logging.info('Disconnecting MQTT client from broker: ' + self.host)
            self.mqttClient.loop_stop()
            self.mqttClient.disconnect()
            
            return True
        else:
            logging.warning('MQTT client already disconnected. Ignoring.')
            
            return False
    
    def onConnect(self, client, userdata, flags, rc):
        logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
    
    def onDisconnect(self, client, userdata, rc):
        logging.info('[Callback] Disconnected from MQTT broker. Result code: ' + str(rc))
    
    def onMessage(self, client, userdata, msg):
        payload = msg.payload
        
        if payload:
            if not self.enablePerformanceTest:
                logging.info('MQTT message received with payload: ' + str(payload.decode("utf-8")))
        else:
            if not self.enablePerformanceTest:
                logging.info('MQTT message received with no payload: ' + str(msg))
    
    def onPublish(self, client, userdata, mid):
        # Lab 10: Disable logging during performance tests
        if not self.enablePerformanceTest:
            logging.info('MQTT message published: ' + str(client))
    
    def onSubscribe(self, client, userdata, mid, granted_qos):
        logging.info('MQTT client subscribed: ' + str(client))
    
    def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        if not resource:
            logging.warning('No topic specified. Cannot publish message.')
            return False
        
        if not msg:
            logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
            return False
        
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        
        # Lab 10: IMPORTANT - wait for each message to be published
        msgInfo = self.mqttClient.publish(topic = resource.value, payload = msg, qos = qos)
        msgInfo.wait_for_publish()
        
        return True
    
    def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        if not resource:
            logging.warning('No topic specified. Cannot subscribe.')
            return False
        
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        
        logging.info('Subscribing to topic %s', resource.value)
        self.mqttClient.subscribe(resource.value, qos)
        
        return True
    
    def unsubscribeFromTopic(self, resource: ResourceNameEnum = None) -> bool:
        if not resource:
            logging.warning('No topic specified. Cannot unsubscribe.')
            return False
        
        logging.info('Unsubscribing from topic %s', resource.value)
        self.mqttClient.unsubscribe(resource.value)
        
        return True
    
    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        return False
