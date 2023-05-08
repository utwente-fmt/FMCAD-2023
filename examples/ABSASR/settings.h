//------------------------------------------------------------------------------
// All settings for the environment model
// for the test cases "Beschleunigungsfahrt" and "Vollbremsung"
// 
// Autor:    Tammo Mathias Stupp
// 
// erstellt: 2008-06-22
// geändert: 2008-07-03
//------------------------------------------------------------------------------

#ifndef __SETTINGS_H__
#define __SETTINGS_H__

//------------------------------------------------------------------------------
// Konstanten
//------------------------------------------------------------------------------
#define TICKPERIOD 1 // period to send ticks from tick counters to ecu (in ms)
#define ABSACTIVE 22 // 21600 mm/s = 22 m/s is 6 km/h

#define lambda_abs 13  // maximum wheel lock is 13 %
#define lambda_asr 13  // maximum slippage is 13 %
#define minus_a -14 //  max. wheel deceleration is 14 m/s2, so 14000 mm/s2
#define plus_a 2  // plus_a is only slightly above 0
#define plus_A 98 // +A = 10 * g = 10 * 9.81 [m/s2] = 98100 [mm/s2]
#define AREF -2 // estimated deceleration on an optimal surface 
                // used to find reference velocity

//#define VELOFACTOR 754 // v = s/t = Ticks/50 * freq * 2 * pi * r = 0.754 * Ticks [m/s] = 754 * Ticks [mm/s]  

#define TASIZE 4 // size of the array for temporary saved ticks 

#endif

