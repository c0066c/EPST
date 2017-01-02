all-print: ./*.py
	python printer_run500.py
	python printer_run500_u70.py
	python dm2_printer_run500.py
	python dm3_printer_run500.py
	python approx_printer.py
	# Here the results are given and constant.

evaluation: ./*.py
	python mp_frVsProb.py 
	# this will finish the tests from 1 to 3 deadline misses with multi-processing
	python mp_frVsProb_dml.py 
	# this is used to evaluate for l-consecutive deadline misses

time: ./*.py
	python timeError.py 
	# use for showing analysis overhead among different approaches

approxerror: ./*.py
	python approxError.py
	# this is used to show the approx. error

sim-approxerror: ./*.py
	python simple_approxError.py
	# this is a simple version with static input for showing the approx. error.
