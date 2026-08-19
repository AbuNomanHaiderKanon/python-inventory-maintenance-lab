# CSE 4802 Lab 3 experiments

Run these commands from the repository root after installing the lab tools:

```powershell
python -m pip install -r requirements-lab.txt
python lab/loguru_demo.py
python lab/pysnooper_demo.py
viztracer -o lab/viztracer_output.json lab/target.py
python -m cProfile -o lab/inventory.profile lab/target.py
snakeviz lab/inventory.profile
```

Outputs are written to `lab/loguru_output.log`, `lab/pysnooper_output.log`,
`lab/viztracer_output.json`, and `lab/inventory.profile`.
