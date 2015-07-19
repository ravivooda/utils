#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdlib.h>
using namespace std;

class Name {
public:
  string first_name;
  string middle_name;
  string last_name;
  string first_initial;
  string middle_initial;
        
  string highestOrderName(){return first_name;}
};

class Record {
public:
  Name* name;
  int ssn;
};

Name* getNameFromSting(string str, Name* existing_){
  size_t f_comma = str.find(",");
  size_t f_space = str.find(" ");
  size_t f_dot = str.find(".");
  Name *name = existing_;
  if (name == 0){
    name = new Name();
  }
  if (f_comma == std::string::npos && f_space == std::string::npos){
    //Its only first name
    name->first_name = str;
  } else if (f_comma != std::string::npos && f_space == std::string::npos){
    name->last_name = str.substr(0, f_comma);
    name->first_name = str.substr(f_comma + 1);
  } else if (f_space != std::string::npos && f_comma == std::string::npos) {
    if (f_dot == std::string::npos){
      name->first_name = str.substr(0, f_space);
      string rest = str.substr(f_space + 1);
      size_t f_sp_space = rest.find(" ");
      if (f_sp_space == std::string::npos){
	name->last_name = rest;
      } else {
	name->middle_name = rest.substr(0, f_sp_space);
	name->last_name = rest.substr(f_sp_space + 1);
      }
    } else {
      string rest = str.substr(f_dot+1);
      size_t f_dot_dot = rest.find(".");
      string middle_name;
      if (f_dot_dot == std::string::npos){
	name->first_name = str.substr(0, f_space);
	middle_name = str.substr(f_space+1, f_dot);
	name->last_name = str.substr(f_dot+2);
      } else {
	name->first_initial = str.substr(0,f_space);
	middle_name = str.substr(f_space+1,f_dot_dot);
	name->last_name = str.substr(f_dot_dot+2);
      }
      name->middle_initial = middle_name;
    }
  } else {
    name->last_name = str.substr(0,f_comma);
    name->first_name = str.substr(f_comma+1,f_space);
    name->middle_name = str.substr(f_space+1);
  }
  return name;
}

void removeDuplicates(string input[], int size){
  cout << "Im called?" << "\n";
  vector<Record*> records;
  map<int, Record*> record_map;
  for (int i = 0; i < size; i++){
    string str = input[i];
    cout << "Error?? \n";
    size_t found = str.find(":");
    cout << "Found str: " << str << "\n";
    if (found != std::string::npos){
      string name = str.substr(0,found);
      int ssn = atoi(str.substr(found+1).c_str());
      cout << "Got Record: " << ssn << " for " << name << "\n";
      map<int, Record*>::iterator iter = record_map.find(ssn);
      if (iter != record_map.end()){
	cout << "Updating record: " << ssn << " for " << name << "\n";
	Record *existing_record = iter->second;
	existing_record->name = getNameFromSting(name, existing_record->name);
      } else {
	cout << "Put new record: " << ssn << " for " << name << "\n";
	Record *new_record = new Record();
	new_record->ssn = ssn;
	new_record->name = getNameFromSting(name, new_record->name);
	record_map[ssn] = new_record;
	records.push_back(new_record);
      }
    }
  }
    
  for (int i = 0; i < records.size(); i++){
    Record *record = records.at(i);
    cout << "SSN: " << record->ssn << "\n";
  }
}

int main() {
  /* Enter your code here. Read input from STDIN. Print output to STDOUT */
  int N;
  cin >> N;
  string input[N];
  for (int i = 0; i < N; i++){
    cin >> input[N];
  }
  removeDuplicates(input, N);
  return 0;
}
