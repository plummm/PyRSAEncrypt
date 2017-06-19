#include <openssl/md5.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

unsigned char * name="ETenal";
unsigned char *md5_result = NULL;
char mdString[33];

int main()
{
md5_result = (unsigned char*)malloc(MD5_DIGEST_LENGTH);
MD5(name,strlen(name),md5_result);
for (int i=0;i<16;i++)
	sprintf(&mdString[i*2], "%02x", (unsigned int)md5_result[i]);
printf("%s",mdString);
}
