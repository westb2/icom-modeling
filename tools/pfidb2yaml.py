from parflow import Run


run_dir = "../runs/tcl_run"
reference_run = 'ELM_re1.pfidb'
run = Run.from_definition(f'{run_dir}/{reference_run}')
run.write(file_format='yaml')
