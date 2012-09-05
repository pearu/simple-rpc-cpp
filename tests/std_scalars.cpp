#include <string>
#include <vector>
#include <list>
#include "std_scalars.hpp"

bool getarg(bool a) { return a; }
char getarg(char a) { return a; }
short getarg(short a) { return a; }
int getarg(int a) { return a; }
long getarg(long a) { return a; }
float getarg(float a) { return a; }
double getarg(double a) { return a; }
std::string getarg(const std::string& a) { return a; }

void passarg(const std::string& a) { ; }

std::vector<char> getarg(const std::vector<char>& a) { return a; }
std::vector<short> getarg(const std::vector<short>& a) { return a; }
std::vector<int> getarg(const std::vector<int>& a) { return a; }
std::vector<long> getarg(const std::vector<long>& a) { return a; }
std::vector<float> getarg(const std::vector<float>& a) { return a; }
std::vector<double> getarg(const std::vector<double>& a) { return a; }
std::vector<std::string> getarg(const std::vector<std::string>& a) { return a; }
std::list<int> getarg(const std::list<int>& a) { return a; }

double sum(const std::vector<double>& a,
	   const std::vector<double>& b,
	   const std::vector<double>& c,
	   const std::vector<double>& d,
	   const std::vector<double>& e,
	   const std::vector<double>& f
	   )
{ 
  double sum = 0;
  for /**/(int i=0; i<a.size(); ++i)
    sum += a[i] + b[i] + c[i] + d[i] + e[i] + f[i];
  return sum; 
}

double sum(const std::vector<double>& a,
	   const std::vector<double>& b
	   )
{ 
  double sum = 0;
  for /**/(int i=0; i<a.size(); ++i)
    sum += a[i] + b[i];
  return sum; 
}

double sum(const std::vector<double>& a
	   )
{ 
  double sum = 0;
  for /**/(int i=0; i<a.size(); ++i)
    sum += a[i];
  return sum; 
}

bool swap(std::vector<double>& a,
	  std::vector<double>& b
	  )
{ 
  double x;
  for /**/(int i=0; i<a.size(); ++i)
    {
      x = a[i];
      a[i] = b[i];
      b[i] = x;
    }
  return true;
}
