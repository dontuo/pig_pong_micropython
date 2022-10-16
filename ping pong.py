#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
//ball
byte ballx = 1;
byte bally = 1;
byte dirx = 1;
byte diry = 1;
byte r = 2;
byte pin_butt = 8;
//racket
int racketx;
byte rackety = 40;
byte width_racket = 10;
//health
int health = 3;
//score
int score;
boolean first = 0;
// Software SPI (slower updates, more flexible pin options):
// pin 7 - Serial clock out (SCLK)
// pin 6 - Serial data out (DIN)
// pin 5 - Data/Command select (D/C)
// pin 4 - LCD chip select (CS)
// pin 3 - LCD reset (RST)
Adafruit_PCD8544 display = Adafruit_PCD8544(7, 6, 5, 4, 3);

void setup() {
  Serial.begin(9600);
  
  display.begin();
  display.setContrast(50);
  display.display();
  delay(2000);
  display.clearDisplay();
  pinMode(pin_butt, INPUT_PULLUP);
}

void loop() {
  while (health){
    if (first){delay(1000); first=0;}
    if (!digitalRead(pin_butt)){health++;}
    Serial.println(score);
    draw_lifes();
    draw_lines();
    draw_platform();
    draw_ball();
    display.display();
    display.clearDisplay();
  }
  if (!digitalRead(pin_butt)){health = 3; first = 1;}
  display.setTextSize(1);
  display.setCursor(0,10);
  display.println("Game over");
  display.setCursor(0,25);
  display.println("Score:");
  display.setCursor(0,35);
  display.println(score);
  display.display();
}



byte check_dir_bally(){
  if (bally + r >= 40 and bally - r <= 39){
      for (byte i = ballx - r; i <= ballx + r; i++){
        for (byte b = 0; b <= width_racket; b++){
          if (i == racketx + b){score ++; return diry * -1; break;}}}}
  else{
    if(bally  - r <= 1){return diry;}
    else if (bally + r >= 47){health--; first++;
    ballx = random(1, 83); bally = random(1, 15);
    delay(500);}}}

byte check_dir_ballx(){
  if (ballx + r >= 83) {return dirx * -1;}
  else if (ballx - r <= 1) {return dirx;}}
  
void draw_ball(){
  ballx += check_dir_ballx();
  bally += check_dir_bally();
  display.fillCircle(ballx,bally,r,1);}
  
void draw_platform(){
  racketx = analogRead(A0);
  racketx = map(racketx, 0, 1023, 1, 84 - width_racket - 1);
  racketx = constrain(racketx, 0, 77);
  display.drawLine(racketx,rackety, racketx + width_racket, rackety, 1);
  display.drawLine(racketx,rackety - 1, racketx + width_racket, rackety - 1, 1);
  randomSeed(racketx);}
  
void draw_lines() {
  display.drawLine(0,0, 0, 47, 1);
  display.drawLine(0,0, 83, 0, 1);
  display.drawLine(0,47, 83, 47, 1);
  display.drawLine(83,0, 83, 47, 1);
  }

void draw_lifes(){
  byte x = 3;
  byte y = 3;
  byte x1 = 2;
  for (byte a = 0; a <= health - 1; a++){
    display.drawPixel(x, 3, 1);
    /*display.display();
    delay(1000);*/
    x += 2; 
    }
  }
