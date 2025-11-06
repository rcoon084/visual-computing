import oscP5.*;
import netP5.*;

OscP5 osc;
NetAddress remote;

float x = 300;
float y = 300;
color bg = color(0);

void setup() {
  size(600, 600);
  frameRate(60);

  osc = new OscP5(this, 9000);         
  remote = new NetAddress("127.0.0.1", 9000);

  println("Waiting OSC from Python...");
  println("Allowed commands: arriba / abajo / izquierda / derecha / rojo / verde / azul");
}

void draw() {
  background(bg);

  fill(255);
  ellipse(x, y, 60, 60);

  x = constrain(x, 30, width  - 30);
  y = constrain(y, 30, height - 30);
}

void oscEvent(OscMessage m) {

  println("OSC:", m.addrPattern(), "→ args:", m.arguments().length, "type:", m.typetag());

  if (m.checkAddrPattern("/move")) {
    try {
      int dx = m.get(0).intValue();
      int dy = m.get(1).intValue();

      x += dx * 20;
      y -= dy * 20;          

      println("MOVE ok", dx, dy);
    } catch(Exception e) {
      println("Error in MOVE", e);
    }
  }

  if (m.checkAddrPattern("/color")) {
    try {
      if (m.arguments().length < 3) {
        println("Invalid parameters");
        return;
      }

      float r = m.get(0).intValue();
      float g = m.get(1).intValue();
      float b = m.get(2).intValue();

      if (r<=1 && g<=1 && b<=1){
        r*=255; g*=255; b*=255;
      }

      bg = color(r,g,b);
      println("COLOR ok", r,g,b);

    } catch(Exception e) {
      println("Error in COLOR", e);
    }
  }
}
