#!/bin/bash

aubio notes test.wav | awk '{if($1  == 91)
print "1";
else if ($1 == 82) 
print "0";
}' | tr -d '\n'
