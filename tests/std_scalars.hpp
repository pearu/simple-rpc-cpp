
#ifndef STD_SCALARS_HPP_DEFINED
#define STD_SCALARS_HPP_DEFINED

#include <string>
#include <vector>

bool getarg(bool a);
char getarg(char a);
short getarg(short a);
int getarg(int a);
long getarg(long a);
float getarg(float a);
double getarg(double a);
std::string getarg(std::string a);
std::vector<char> getarg(std::vector<char>& a);
std::vector<short> getarg(std::vector<short>& a);
std::vector<int> getarg(std::vector<int>& a);
std::vector<long> getarg(std::vector<long>& a);
std::vector<float> getarg(std::vector<float>& a);
std::vector<double> getarg(std::vector<double>& a);
std::vector<std::string> getarg(std::vector<std::string>& a);

#endif
