One of the previous works done on Visual Tasks include https://smlab.niser.ac.in/labtalks/talks/orb-slam3/

the lens.ipynb notebook contains the code implementations of the various models generally used for the CBIR task.

A Draft Review/Report file is provided along with a react app to try out the models.

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd frontend
npm start
```

Download the CalTech 101 dataset and extract into the frontend/public folder.
