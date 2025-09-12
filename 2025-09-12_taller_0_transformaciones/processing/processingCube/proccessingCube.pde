// setup() runs once at the beginning.
void setup() {
  // Create a 800x600 canvas with the 3D rendering engine.
  size(800, 600, P3D); 
}

// draw() runs in a loop, redrawing the screen on each frame.
void draw() {
  // Clear the background on each frame with a dark color.
  background(20, 20, 40); 
  // Add default lighting to the 3D scene.
  lights();
  
  // Save the current state of the coordinate system.
  pushMatrix();
  
  // Apply a wavy translation on the x-axis.
  float waveX = sin(frameCount * 0.02) * 150;
  translate(width / 2 + waveX, height / 2, 0);
  
  // Apply constant rotation on the Y and X axes.
  float angle = frameCount * 0.01;
  rotateY(angle);
  rotateX(angle * 0.5);
  
  // Apply cyclic scaling for a pulsing effect.
  float scaleFactor = 1.0 + 0.5 * sin(frameCount * 0.05);
  scale(scaleFactor);
  
  // Draw the object in the already transformed system.
  noStroke();
  fill(100, 120, 255);
  box(120);
  
  // Restore the coordinate system to its previous state.
  popMatrix();
}
