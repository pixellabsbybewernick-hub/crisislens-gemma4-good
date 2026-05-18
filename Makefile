.PHONY: install run test demo

install:
	python -m pip install -r requirements.txt

run:
	streamlit run app.py

test:
	pytest -q

demo:
	streamlit run app.py --server.headless true
