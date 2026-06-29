\# Hospital Patient Data Analysis



A real-world data cleaning and analysis project using Python and pandas — built for the DataPeaks Solutions YouTube series on practical data analytics.



Watch the full walkthrough on YouTube: \*\[add your video link here]\*



\## What this project covers



Real hospital data is never clean. This project works with a 20-patient, 12-column dataset that has missing discharge dates, missing length-of-stay values, and missing bill amounts — and shows how to handle that the right way.



\- \*\*Load \& inspect\*\* — find exactly where the gaps are before touching anything

\- \*\*Clean the data\*\* — department-wise median imputation instead of a misleading global average, plus context-aware handling for patients still admitted

\- \*\*Analyse by department\*\* — patient volume, average length of stay, and revenue via `groupby().agg()`

\- \*\*Payment mode breakdown\*\* — Insurance vs. Cash vs. Government split

\- \*\*Final summary\*\* — a complete picture of the dataset in a few printed lines



\## Files



| File | Description |

|---|---|

| `analysis.py` | Full analysis pipeline — run this |

| `data.csv` | The hospital patient dataset |



\## How to run it



```bash

pip install pandas

python analysis.py

```



You'll see the full breakdown printed to your terminal in under a minute.



\## Use your own data



Swap in your own dataset with the same column structure (`PatientID`, `Age`, `Department`, `Diagnosis`, `LOS\_Days`, `Bill\_Amount`, `Payment\_Mode`, `Status`, etc.) and the pipeline works identically.



\## More from DataPeaks Solutions



New real-world data analytics projects every week — Python, SQL, Power BI, and Machine Learning, with healthcare and pharma domain context.



\- Website: \[datapeakssolutions.com](https://datapeakssolutions.com)

\- Instagram: \[@datapeaks\_solutions](https://instagram.com/datapeaks\_solutions)

\- YouTube: \[@datapeakssolutions](https://youtube.com/@datapeakssolutions)

