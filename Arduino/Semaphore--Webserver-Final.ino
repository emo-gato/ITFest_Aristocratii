#include "WiFi.h"
#include "ESPAsyncWebServer.h"
 
struct semaphore{
  int red;
  int green;

  void switchToOff(){
    digitalWrite(green,LOW);
    digitalWrite(red,LOW);
  }

  void switchToRed(){
    digitalWrite(green,LOW);
    digitalWrite(red,HIGH);
  }

  void switchToGreen(){
    digitalWrite(red,LOW);
    digitalWrite(green,HIGH);
  }

  void turnAllOn(){
    digitalWrite(red,HIGH);
    digitalWrite(green,HIGH);
  }

  void cycle(){
    switchToRed();
    delay(2000);
    switchToGreen();
    delay(2000);
  }

  semaphore(int redPin,int greenPin){
    red = redPin;
    green = greenPin;
    pinMode(red,OUTPUT);
    pinMode(green,OUTPUT);
  }

  semaphore(){}
};


const char* ssid = "Xiaomi 11 Lite";
const char* password =  "alexphone";
 
AsyncWebServer server(80);

struct semaphore s0,s1,s2,s3;

 
void semaphoreHandling(AsyncWebParameter* p){
  struct semaphore sUsed;
  if(p->name().compareTo("s0")==0)
    sUsed = s0;
  else if(p->name().compareTo("s1")==0)
    sUsed = s1;
  else if(p->name().compareTo("s2")==0)
    sUsed = s2;
  else if(p->name().compareTo("s3")==0)
    sUsed = s3;


  switch(p->value().toInt()){
    case 0:
    sUsed.switchToOff();
    break;
    case 1:
    sUsed.switchToRed();
    break;
    case 2:
    sUsed.switchToGreen();
    break;
  }

}

void semaphoresInitialization(){
  s0 = semaphore(27,26); //alb
  Serial.println("Semaphore 0 Initialized\n");
  s3 = semaphore(12,13); //albastru
  Serial.println("Sempahore 1 Initialized\n");
  s1 = semaphore(25,14); //rgb
  Serial.println("Semaphore 2 Initialized\n");
  s2 = semaphore(33,32); //galben
  Serial.println("Semaphore 3 Initialized\n");
}

void serverInitialization(){
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println(WiFi.localIP());
  server.begin();
}


void semaphoreRequestHandling(){
    server.on("/semaphore", HTTP_GET, [](AsyncWebServerRequest *request){
      int paramsNr = request->params();
      for(int i=0;i<paramsNr;i++){
        semaphoreHandling(request->getParam(i));
      }
      request->send(200, "text/plain", "message received");
    }
  );
}
void defaultCycle()
{
  while(1){
    s0.switchToGreen();
  s2.switchToGreen();
  s1.switchToRed();
  s3.switchToRed();
  delay(2000);
  s1.switchToGreen();
  s3.switchToGreen();
  s0.switchToRed();
  s2.switchToRed();
  delay(2000);
  }
}


void defaultSempahore(){
  server.on("/semaphoreDefault", HTTP_GET, [](AsyncWebServerRequest *request){
    defaultCycle();
    request->send(200, "text/plain", "message received");
    }
  );
}


void setup(){
  Serial.begin(115200);
  semaphoresInitialization();
  serverInitialization();
  semaphoreRequestHandling();
  defaultSempahore();
}
//TODO: CREATE THE SEMAPHORE HANDLEING 
//TOOD: TEST EVERYTHING WORKS
//TODO: ANNOY TEO TO TEST THE REQUESTS
//TODO: MAYBE ADD SOME LEDs FOR VISUALISATION
//TODO: DEF REWIRE EVERYTHING UNDER THE LEGO SO IT LOOKS CLEAN  

void loop(){
}
