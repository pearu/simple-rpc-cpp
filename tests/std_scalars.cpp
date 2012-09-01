#include <string>
#include <vector>
#include "std_scalars.hpp"

bool getarg(bool a) { return a; }
char getarg(char a) { return a; }
short getarg(short a) { return a; }
int getarg(int a) { return a; }
long getarg(long a) { return a; }
float getarg(float a) { return a; }
double getarg(double a) { return a; }
std::string getarg(std::string a) { return a; }

std::vector<char> getarg(std::vector<char>& a) { return a; }
std::vector<short> getarg(std::vector<short>& a) { return a; }
std::vector<int> getarg(std::vector<int>& a) { return a; }
std::vector<long> getarg(std::vector<long>& a) { return a; }
std::vector<float> getarg(std::vector<float>& a) { return a; }
std::vector<double> getarg(std::vector<double>& a) { return a; }
std::vector<std::string> getarg(std::vector<std::string>& a) { return a; }
