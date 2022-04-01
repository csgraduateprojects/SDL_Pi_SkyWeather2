
import config
import state
import buildJSON

import paho.mqtt.client as paho
from paho import mqtt

def on_publish(client, userdata, mid, properties=None):
    print(f'mid: {mid}')
    print("message published")

def on_disconnect(client, userdata, rc, properties=None):
    if rc == paho.MQTT_ERR_SUCCESS:
        print("Disconnected successfully")
    else:
        print("Unexpected disconect")

def connectMQTTBroker():
    state.mqtt_client = paho.Client(client_id="SkyWeather2", protocol=paho.MQTTv5)
    state.mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    state.mqtt_client.username_pw_set("vineyard", "R0b0tslab")
    state.mqtt_client.connect(config.MQTT_Server_URL, port=config.MQTT_Port_Number)

def publish():
    """
    Function connects to a MQTT broker and send message, then disconnects from broker
    """
    if (config.SWDEBUG):
        print("--->Sending MQTT Packet<---")
        state.mqtt_client.on_publish = on_publish
        state.mqtt_client.on_disconnect = on_disconnect

    #connect to broker
    connectMQTTBroker()

    state.mqtt_client.loop_start()

    #Get semaphore first so we don't have a halfway read issue
    state.buildJSONSemaphore.acquire()
    #print("buildJSONSemaphore Acquired")
    #---don't think we need this state.StateJSON = buildJSON.getStateJSON()
    #if (config.SWDEBUG):
    #    print("currentJSON = ", state.StateJSON)
    #Get all the state readings
    all_states = buildJSON.getStateJSON_all()
    state.buildJSONSemaphore.release()
    #print("buildJSONSemaphore Released")for single_state in all_states: 

    #Just for testing
    for single_state in all_states:
    #if len(all_states) > 1:
        #single_state = all_states[0]
        #print("Going to publish")
        #print(single_state)
        #print(type(single_state))
        msgpub = state.mqtt_client.publish("skyweather2/state", single_state)

        #check if sent
        if msgpub.rc != paho.MQTT_ERR_SUCCESS:
            print("Publish unsuccessful")
        #print(msgpub.rc)
        msgpub.wait_for_publish()

    #start disconnect sequence 
    #msgpub.wait_for_publish()
    state.mqtt_client.loop_stop()
    state.mqtt_client.disconnect()

def mqtt_publish_single(message, topic):
   topic = '{0}/{1}'.format("skyweather2", topic)
    
   #connect to broker
   connectMQTTBroker()

   #print("topic=", topic)
   try:
        state.mqtt_client.loop_start()
        msgpub = state.mqtt_client.publish(topic, message)

        #start disconnect sequence
        msgpub.wait_for_publish()
        state.mqtt_client.loop_stop()
        state.mqtt_client.disconnect()

   except:
        traceback.print_exec()
        print('Mosquitto not available')
