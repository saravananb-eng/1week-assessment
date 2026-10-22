import csv
import io

CSV_DATA = """id,name,department,salary,city
1,Arun,Sales,30000,chennai
2,Priya,HR,45000,chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,chennai
5,karthik,Finance,90000,Mumbai
6,Menna,Sales,52000,Bangalore
7,suresh,IT,68000,chennai
8,Anitha,HR,48000,Mumbai  
"""
rows =list(csv.DictReader(io.StringIO(CSV_DATA)))
for r in rows:
    r["id"]=int(r["id"])
    r["salary"]=int(r["salary"])

def bonus(salary,rate=0.1,*extras,**options):
    result=salary*rate+sum(extras)
    if"cap"in options:
        result= min(result,options["cap"])
        return result

class InvalidSalaryError(Exception):
    pass

class Employee:
    
    def __init__(self,name,salary):
     if salary< 0 :
        raise InvalidSalaryError(f"invalid salary:{salary}")
     self.name= name
     self.salary= salary

def annual_salary(self):
   return self.salary* 12

def get_details(self):
   return f"{self.name}earns{self.salary}per month"

class Manager(Employee):
   def __init__(self, name,salary,teamsize):
      super().__init__(name,salary)
      self.team_size= team_size

def get_details(self):
   return f"{super().get_details()}and manages {self.team_size}people"

above_50000 =[r["name"] for r in rows if r["salary"]>50000]
print("above 50000:",above_50000)

raised =map(lambda r:{**r,"salary":r["salary"]*1.1},rows)
chennai =list(filter(lambda r:r["city"]=="chennai",raised))
print("chennai:",[r["name"]for r in chennai])

try:
   Employee("Test",-500)
except InvalidSalaryError as e:
   print("Error:",e)
finally:
   print("Transaction finished")


   salaries =[30000,0,45000,60000,90000,52000]
   for s in salaries:
    if s==0:
       continue
    if s> 85000:
       break
