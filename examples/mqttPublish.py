from ClauLib.clau import Clau
import paho.mqtt.client as mqtt
import json, time

class Cliente:

    def __init__(self, name = "Clau"):
        self.name = name
        self.mqttStatus = False

    def init_mqtt(self, 
                   host = "localhost", 
                   port = 1883, 
                   topic = "CLAU", 
                   client_id = "clau_client",
                   keepalive = 20,
                   username = "admin",
                   password = "public"):
        if self.mqttStatus:
            self.stop_mqtt()
        try:
            self.client = mqtt.Client(client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            clean_session=False)
            self.client.username_pw_set(username, password)
            self.client.connect(host, port, keepalive)
            
            #self.client.connect_async(host, port, keepalive)
            #self.client.loop_start()

            array_topic = topic.split("/")
            array_topic = [s for s in array_topic if s != ""]
            clean_topic  = "/".join(array_topic)
            self.topic = clean_topic+f"/{self.name}"
            self.mqttStatus = True
            return self.topic
        except:
            raise Exception("Fallo al conectarse")
    
    def disconect_mqtt(self):
        if self.mqttStatus:
            self.client.disconnect()
            self.mqttStatus = False
            return True
        return False

    def publish(self, data = {"status": True}):
        if not self.mqttStatus: return
        #Convertir a json
        msg = json.dumps(data)
        #Enviar con qos 0 
        return self.client.publish(self.topic, msg, qos=0)

def main():
    #clau = Clau(port="COM5", n_data=10)
    #st = clau.calibrate()
    #print(st)
    client = Cliente(name="test")
    
    client.init_mqtt(
        host="localhost",     # porque el contenedor expone el puerto 1883 al host
        port=1883,            # puerto MQTT estándar
        topic="Test",         # topic base
        client_id="cliente_local",
        username="admin",     # credenciales por defecto de EMQX
        password="Dr-1203909-emqx"
    )
    i = 1
    while True:
        msg = {"Temperature":i}
        topic = "Test/test"
        result = client.publish(msg)
        status = result[0]
        print()
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`", flush=True)
        else:
            print(f"Failed to send message to topic {topic}", flush=True)
        i += 1
        time.sleep(2)

main()