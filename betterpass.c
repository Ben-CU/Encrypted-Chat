#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>

int IsDebuggerPresent(void)
{
/*
Checks to see if this program is being run through a debugger like gdb
one of the answers from:
http://stackoverflow.com/questions/3596781/how-to-detect-if-the-current-process-is-being-run-by-gdb
*/
    char buf[1024];
    int debugger_present = 0;
    int status_fd = open("/proc/self/status", O_RDONLY);
    if (status_fd == -1)
        return 0;
    ssize_t num_read = read(status_fd, buf, sizeof(buf));
    if (num_read > 0)
    {
        static const char TracerPid[] = "TracerPid:";
        char *tracer_pid;
        buf[num_read] = 0;
        tracer_pid    = strstr(buf, TracerPid);
        if (tracer_pid)
            debugger_present = !!atoi(tracer_pid + sizeof(TracerPid) - 1);
    }
    return debugger_present;
}

int main()
{ 
/*
Checks for a debugger if there is the program exits otherwise will run as normal
*/
 if (IsDebuggerPresent())
 {
  printf("Fatal Error! The debugger will now exit.");
 }
 else
 {
/*
This section creates most of the variables used
*/
  char UserInput[7];
  printf ("Please enter the password: ");
  fgets(UserInput, 7, stdin);
  long PassKey = 1946252954870; //Password stored as a number
  int InputLength = strlen(UserInput);
  int NumberArray[InputLength];
  int Counter;
  long UsersFirstKey = 1;
  char SecretStuff[] = "tDKBNLDySNySGDyRDBQDSyLzMHEDRSNyxykDUDQyRGNVySNyNSGDQRy"; //The encrypted secret information
/*
The two keys used to see if the password was correct are created in the section below
*/
  for (Counter = 0; Counter < InputLength; Counter++)
  {
    NumberArray[Counter] = UserInput[Counter];
    UsersFirstKey = UsersFirstKey * NumberArray[Counter] + NumberArray[Counter]; //The first key is worked out this way
  }
  long UsersSecondKey = UsersFirstKey; // The second key becomes equal to the first
  while (UsersSecondKey > 53)
  {
    UsersSecondKey = UsersSecondKey % 53; // if the second key is bigger than 53 the remainder is taken after dividing by 53
  }
/*
if the password the user == the passkey then the SecretInformation is decoded based on the second key in the section below
*/
  if (PassKey == UsersFirstKey)
  {
    char CharList[] = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-)"; // The characters that were used to encrypt the secret information
    char DecodedSecretStuff[strlen(SecretStuff)]; 
    for (Counter = 0; Counter < strlen(SecretStuff); Counter++)
    {
      int CurrentPosition = 0;
      while (SecretStuff[Counter] != CharList[CurrentPosition])
      {
        CurrentPosition++; //runs through the CharList that character is the same as the one in secret stuff the index is then stored in CurrentPosition
      }
      CurrentPosition -= UsersSecondKey;
      if (CurrentPosition < 0)
      {
        DecodedSecretStuff[Counter] = CharList[CurrentPosition + strlen(CharList) - 1]; //If CurrentPosition is smaller than 0 then the size of Charlist is added to it -1
      }
      else
      {
        DecodedSecretStuff[Counter] = CharList[CurrentPosition];
      }
    }
    printf ("%s\n", DecodedSecretStuff);
  }
  else
  {
    printf ("Sorry that Password is incorrect, stay away.\n");
  }
 return 0;
 }
}
