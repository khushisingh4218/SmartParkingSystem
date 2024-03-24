#include <AFMotor.h>
//#define CUSTOM_SETTINGS
//#define INCLUDE_GAMEPAD_MODULE
//#include <Dabble.h>


//initial motors pin
AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);
AF_DCMotor motor3(3, MOTOR34_1KHZ);
AF_DCMotor motor4(4, MOTOR34_1KHZ);
char inp;


void setup()
{

//  Dabble.begin(9600, 9, 10);
    Serial.begin(9600);

}


void loop() {

      while (Serial.available() > 0)
        {
//          delay(10);
//          char c = Serial.read();
//          if (c == '#')
//          {
//            break;
//          }
//          inp += c;

        inp=Serial.read();
        Serial.print(inp);
        
        
        if (inp == 'F' )
        {
          forward();
        }
        else if (inp == 'B')
        {
          back();
        }
        else if (inp == 'L')
        {
          left();
        }
        else if (inp == 'R')
        {
          right();
        }
        else if (inp == 'S')
        {
          Stop();
        }
        
      
//        if (inp.length() > 0)
//        {
//          Serial.println(inp);
//          inp = "";
//          Stop();
//        }
        
        delay(10);
        
        }

        }
      
        
  
//  Dabble.processInput();
//  if (GamePad.isUpPressed())
//  {
//    forward();
//  }
//
//  if (GamePad.isDownPressed())
//  {
//    back();
//
//  }
//
//  if (GamePad.isLeftPressed())
//  {
//    left();
//
//  }
//
//  if (GamePad.isRightPressed())
//  {
//    right();
//
//  }
//
//  if (GamePad.isCrossPressed())
//  {
//    Stop();
//
//  }



void forward()
{
  motor1.setSpeed(255); //Define maximum velocity
  motor1.run(FORWARD);  //rotate the motor clockwise
  motor2.setSpeed(255); //Define maximum velocity
  motor2.run(FORWARD);  //rotate the motor clockwise
  motor3.setSpeed(255); //Define maximum velocity
  motor3.run(FORWARD);  //rotate the motor clockwise
  motor4.setSpeed(255); //Define maximum velocity
  motor4.run(FORWARD);  //rotate the motor clockwise
}

void back()
{
  motor1.setSpeed(255); //Define maximum velocity
  motor1.run(BACKWARD); //rotate the motor anti-clockwise
  motor2.setSpeed(255); //Define maximum velocity
  motor2.run(BACKWARD); //rotate the motor anti-clockwise
  motor3.setSpeed(255); //Define maximum velocity
  motor3.run(BACKWARD); //rotate the motor anti-clockwise
  motor4.setSpeed(255); //Define maximum velocity
  motor4.run(BACKWARD); //rotate the motor anti-clockwise
}

void left()
{
  motor1.setSpeed(255); //Define maximum velocity
  motor1.run(BACKWARD); //rotate the motor anti-clockwise
  motor2.setSpeed(255); //Define maximum velocity
  motor2.run(BACKWARD); //rotate the motor anti-clockwise
  motor3.setSpeed(255); //Define maximum velocity
  motor3.run(FORWARD);  //rotate the motor clockwise
  motor4.setSpeed(255); //Define maximum velocity
  motor4.run(FORWARD);  //rotate the motor clockwise
}

void right()
{
  motor1.setSpeed(255); //Define maximum velocity
  motor1.run(FORWARD);  //rotate the motor clockwise
  motor2.setSpeed(255); //Define maximum velocity
  motor2.run(FORWARD);  //rotate the motor clockwise
  motor3.setSpeed(255); //Define maximum velocity
  motor3.run(BACKWARD); //rotate the motor anti-clockwise
  motor4.setSpeed(255); //Define maximum velocity
  motor4.run(BACKWARD); //rotate the motor anti-clockwise
}

void Stop()
{
  motor1.setSpeed(0);  //Define minimum velocity
  motor1.run(RELEASE); //stop the motor when release the button
  motor2.setSpeed(0);  //Define minimum velocity
  motor2.run(RELEASE); //rotate the motor clockwise
  motor3.setSpeed(0);  //Define minimum velocity
  motor3.run(RELEASE); //stop the motor when release the button
  motor4.setSpeed(0);  //Define minimum velocity
  motor4.run(RELEASE); //stop the motor when release the button
}