all-print: ./*.py
	python printer_run500.py
	python printer_run500_u70.py
	python dm2_printer_run500.py
	python dm3_printer_run500.py
# here the results are constant.

evaluation: ./*.py
	python mp_frVsProb.py &
# this will finish the testing from 1 to 3 deadline misses with multi-processing

time: ./*.py
	python frVsProb.py #use for showing timing

test: ./*.py
	python prob_test.py

approxerror: ./*.py
	python approxError.py
