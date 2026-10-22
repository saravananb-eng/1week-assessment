import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))


marks = np.array([[78, 85, 90], [65, 70, 72], [88, 92, 95], [55, 60, 58]])
print("Shape:", marks.shape)
print("Student averages:", marks.mean(axis=1))
print("Subject averages:", marks.mean(axis=0))
print("With 5 grace marks (broadcasting):\n", marks + 5)
print("Weighted scores:", np.dot(marks, [0.5, 0.3, 0.2]))

raw = pd.read_csv("employees.csv")
raw.info()
print(raw.describe())
print(raw.loc[0:2, ["name", "salary"]])
print(raw.iloc[:3, :3])
print(raw[raw["salary"] > 50000])

df = raw.drop_duplicates().copy()
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["salary"] = df["salary"].fillna(df["salary"].median()).astype(int)
df = df.astype({"experience": int, "join_year": int}).reset_index(drop=True)
print(f"Rows: {len(raw)} -> {len(df)}\n{df.dtypes}")

summary = df.groupby("department").agg(
    headcount=("id", "count"), avg_salary=("salary", "mean"),
    max_salary=("salary", "max")).reindex(["Sales", "HR", "IT", "Finance"])
print(summary)
print("Headcount: " + " | ".join(f"{d} {n}" for d, n in summary["headcount"].items()))
depts = pd.read_csv("departments.csv")
for how in ["inner", "left", "outer"]:
    print(f"{how} join rows:", len(pd.merge(df, depts, on="department", how=how)))
outer = pd.merge(df, depts, on="department", how="outer")
print("Outer join:\n", outer[["department", "name", "salary", "head"]])
print("No employees:", outer[outer["name"].isna()]["department"].tolist())

def finish(title, xlabel, ylabel, fname):
    plt.title(title); plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.legend(); plt.tight_layout(); plt.savefig(fname, dpi=120); plt.close()

plt.bar(summary.index, summary["avg_salary"], label="Average salary")
finish("Average Salary by Department", "Department", "Salary", "bar.png")

plt.hist(df["salary"], bins=5, edgecolor="black", label="Employees")
finish("Salary Distribution", "Salary", "Employees", "hist.png")

for d, g in df.groupby("department"):
    plt.scatter(g["experience"], g["salary"], s=70, label=d)
finish("Experience vs Salary", "Experience (years)", "Salary", "scatter.png")

by_year = df.groupby("join_year")["salary"].mean()
plt.plot(by_year.index, by_year.values, marker="o", label="Average salary")
plt.xticks(by_year.index)
finish("Average Salary by Joining Year", "Joining year", "Salary", "line.png")

print("\nInsights:")
print(f"Bar: {summary['avg_salary'].idxmax()} has the highest average salary.")
print(f"Histogram: {(df['salary'] < 60000).sum()} of {len(df)} employees earn below 60,000.")
print(f"Scatter: experience-salary correlation is {df['experience'].corr(df['salary']):.2f}, so more experience means higher pay.")
print(f"Line: earliest joiners ({by_year.index[0]}) average {by_year.iloc[0]:,.0f} vs {by_year.iloc[-1]:,.0f} for the latest ({by_year.index[-1]}).")
