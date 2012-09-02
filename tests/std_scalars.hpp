
#ifndef STD_SCALARS_HPP_DEFINED
#define STD_SCALARS_HPP_DEFINED

#include <string>
#include <vector>
#include <list>

bool getarg(bool a);
char getarg(char a);
short getarg(short a);
int getarg(int a);
long getarg(long a);
float getarg(float a);
double getarg(double a);
std::string getarg(const std::string& a);
void passarg(const std::string& a);
std::vector<char> getarg(const std::vector<char>& a);
std::vector<short> getarg(const std::vector<short>& a);
std::vector<int> getarg(const std::vector<int>& a);
std::vector<long> getarg(const std::vector<long>& a);
std::vector<float> getarg(const std::vector<float>& a);
std::vector<double> getarg(const std::vector<double>& a);
std::vector<std::string> getarg(const std::vector<std::string>& a);
std::list<int> getarg(const std::list<int>& a);

#endif
