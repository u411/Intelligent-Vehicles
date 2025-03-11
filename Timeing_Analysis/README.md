# Response Time Calculation for Periodic Messages

## Overview

This Python script calculates the response time for a set of periodic messages in a system, considering their priority, execution time, and period. The system uses a schedulability analysis method based on response-time analysis. The input is read from a file `input.dat`, and the output is the response times of each message, printed to the console.

## Functionality

- **Input**: The script reads the following data from an input file `input.dat`:
  - **n**: The number of messages.
  - **tau**: A constant time shift value.
  - A list of `n` messages, each with:
    - **Pi**: The priority of the message (integer).
    - **Ci**: The execution time of the message (float).
    - **Ti**: The period of the message (float).

- **Output**: The script calculates the response time for each message and outputs it as a rounded float value.
