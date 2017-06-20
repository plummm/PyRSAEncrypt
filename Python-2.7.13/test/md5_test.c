#include <dirent.h> 
#include <stdio.h> 

int main(void)
{
  DIR           *d;
  struct dirent *dir;
  d = opendir(".");
  if (d)
  {
    while ((dir = readdir(d)) != NULL)
    {
      printf("filename:%s\n", dir->d_name);
      char *dot = strrchr(dir->d_name, '.');
      if (dot==NULL)
	continue;
      printf("extension:%s\n", dot+1);
      if (strlen(dot+1)==3 && strcmp(dot+1,"pyc")==0)
	{
		printf("find one!\n");
		//remove(dir->d_name)
	}
	
    }

    closedir(d);
  }

  return(0);
}
